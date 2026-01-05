# core/tasks.py
"""
Celery Tasks - фоновые задачи.

Celery - это система для выполнения задач в фоне (асинхронно).
Например: отправка email, обновление tracking, генерация отчетов.

Запуск worker: celery -A config worker -l info
Запуск beat (планировщик): celery -A config beat -l info
"""
import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


# ===========================================
# EMAIL TASKS
# ===========================================

@shared_task(bind=True, max_retries=3)
def send_email_task(self, subject, message, recipient_email, html_message=None):
    """
    Отправка email в фоне.
    
    Использование:
        send_email_task.delay("Subject", "Message", "user@example.com")
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email sent to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {e}")
        self.retry(exc=e, countdown=60 * (self.request.retries + 1))


@shared_task
def send_welcome_email(user_id):
    """Отправить приветственное письмо новому пользователю."""
    from accounts.models import User
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return
    
    subject = _("Willkommen bei BlisterPerPost!")
    html_message = render_to_string("emails/welcome.html", {"user": user})
    message = f"Hallo {user.first_name}, willkommen bei BlisterPerPost!"
    
    send_email_task.delay(subject, message, user.email, html_message)


@shared_task
def send_order_confirmation(order_id):
    """Отправить подтверждение заказа."""
    from deliveries.models import BlisterOrder
    
    try:
        order = BlisterOrder.objects.select_related("user").get(id=order_id)
    except BlisterOrder.DoesNotExist:
        return
    
    subject = _("Ihre Bestellung %(order_number)s wurde bestätigt") % {
        "order_number": order.order_number
    }
    html_message = render_to_string("emails/order_confirmation.html", {"order": order})
    message = f"Ihre Bestellung {order.order_number} wurde bestätigt."
    
    send_email_task.delay(subject, message, order.user.email, html_message)


@shared_task
def send_shipping_notification(shipment_id):
    """Отправить уведомление об отправке."""
    from deliveries.models import Shipment
    
    try:
        shipment = Shipment.objects.select_related("order", "order__user").get(id=shipment_id)
    except Shipment.DoesNotExist:
        return
    
    user = shipment.order.user
    subject = _("Ihre Bestellung wurde versendet!")
    html_message = render_to_string("emails/shipping_notification.html", {
        "shipment": shipment,
        "order": shipment.order,
        "user": user,
    })
    message = f"Ihre Bestellung wurde versendet. Sendungsnummer: {shipment.tracking_number}"
    
    send_email_task.delay(subject, message, user.email, html_message)


@shared_task
def send_payment_failed_notification(user_id, payment_id):
    """Уведомление о неудачном платеже."""
    from accounts.models import User
    from subscriptions.models import Payment
    
    try:
        user = User.objects.get(id=user_id)
        payment = Payment.objects.get(id=payment_id)
    except (User.DoesNotExist, Payment.DoesNotExist):
        return
    
    subject = _("Zahlung fehlgeschlagen")
    html_message = render_to_string("emails/payment_failed.html", {
        "user": user,
        "payment": payment,
    })
    message = "Leider konnte Ihre letzte Zahlung nicht verarbeitet werden."
    
    send_email_task.delay(subject, message, user.email, html_message)


@shared_task
def send_subscription_ending_reminder(subscription_id):
    """Напоминание об окончании подписки."""
    from subscriptions.models import Subscription
    
    try:
        subscription = Subscription.objects.select_related("user", "plan").get(id=subscription_id)
    except Subscription.DoesNotExist:
        return
    
    subject = _("Ihr Abonnement endet bald")
    html_message = render_to_string("emails/subscription_ending.html", {
        "subscription": subscription,
        "user": subscription.user,
    })
    message = f"Ihr Abonnement endet am {subscription.current_period_end.strftime('%d.%m.%Y')}."
    
    send_email_task.delay(subject, message, subscription.user.email, html_message)


# ===========================================
# DHL TRACKING TASKS
# ===========================================

@shared_task
def update_shipment_tracking_task(shipment_id):
    """Обновить tracking для одной посылки."""
    from deliveries.models import Shipment
    from deliveries.services.dhl import update_shipment_tracking
    
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return
    
    success = update_shipment_tracking(shipment)
    
    # Если доставлено - отправляем уведомление
    if success and shipment.status == "delivered":
        send_delivery_confirmation.delay(shipment_id)
    
    return success


@shared_task
def update_all_active_shipments():
    """
    Обновить tracking для всех активных посылок.
    Запускается по расписанию (каждые 2 часа).
    """
    from deliveries.models import Shipment
    
    active_statuses = [
        Shipment.Status.LABEL_CREATED,
        Shipment.Status.PICKED_UP,
        Shipment.Status.IN_TRANSIT,
        Shipment.Status.OUT_FOR_DELIVERY,
    ]
    
    shipments = Shipment.objects.filter(
        status__in=active_statuses,
        tracking_number__isnull=False,
    )
    
    updated = 0
    for shipment in shipments:
        update_shipment_tracking_task.delay(shipment.id)
        updated += 1
    
    logger.info(f"Queued {updated} shipments for tracking update")
    return updated


@shared_task
def send_delivery_confirmation(shipment_id):
    """Отправить подтверждение доставки."""
    from deliveries.models import Shipment
    
    try:
        shipment = Shipment.objects.select_related("order", "order__user").get(id=shipment_id)
    except Shipment.DoesNotExist:
        return
    
    user = shipment.order.user
    subject = _("Ihre Lieferung wurde zugestellt!")
    html_message = render_to_string("emails/delivery_confirmation.html", {
        "shipment": shipment,
        "order": shipment.order,
        "user": user,
    })
    message = f"Ihre Bestellung {shipment.order.order_number} wurde zugestellt."
    
    send_email_task.delay(subject, message, user.email, html_message)


# ===========================================
# SUBSCRIPTION TASKS
# ===========================================

@shared_task
def check_expiring_subscriptions():
    """
    Проверить подписки, которые скоро истекут.
    Запускается ежедневно.
    """
    from subscriptions.models import Subscription
    
    # Подписки, истекающие через 3 дня
    expiring_date = timezone.now() + timedelta(days=3)
    
    subscriptions = Subscription.objects.filter(
        status=Subscription.Status.ACTIVE,
        cancel_at_period_end=True,
        current_period_end__date=expiring_date.date(),
    )
    
    for sub in subscriptions:
        send_subscription_ending_reminder.delay(sub.id)
    
    logger.info(f"Sent {subscriptions.count()} subscription ending reminders")
    return subscriptions.count()


@shared_task
def check_trial_ending():
    """
    Проверить trial подписки, которые скоро истекут.
    Запускается ежедневно.
    """
    from subscriptions.models import Subscription
    
    # Trial, заканчивающийся через 3 дня
    ending_date = timezone.now() + timedelta(days=3)
    
    subscriptions = Subscription.objects.filter(
        status=Subscription.Status.TRIALING,
        trial_end__date=ending_date.date(),
    )
    
    for sub in subscriptions:
        send_trial_ending_reminder.delay(sub.id)
    
    return subscriptions.count()


@shared_task
def send_trial_ending_reminder(subscription_id):
    """Напоминание об окончании trial."""
    from subscriptions.models import Subscription
    
    try:
        subscription = Subscription.objects.select_related("user", "plan").get(id=subscription_id)
    except Subscription.DoesNotExist:
        return
    
    subject = _("Ihre Testphase endet bald")
    html_message = render_to_string("emails/trial_ending.html", {
        "subscription": subscription,
        "user": subscription.user,
    })
    message = f"Ihre Testphase endet am {subscription.trial_end.strftime('%d.%m.%Y')}."
    
    send_email_task.delay(subject, message, subscription.user.email, html_message)


# ===========================================
# ORDER TASKS
# ===========================================

@shared_task
def create_scheduled_orders():
    """
    Создать заказы для активных подписок.
    Запускается ежедневно.
    """
    from deliveries.models import BlisterOrder
    from subscriptions.models import Subscription
    
    # Подписки, у которых период заканчивается завтра
    tomorrow = timezone.now() + timedelta(days=1)
    
    subscriptions = Subscription.objects.filter(
        status=Subscription.Status.ACTIVE,
        current_period_end__date=tomorrow.date(),
    ).select_related("user", "plan")
    
    created = 0
    for sub in subscriptions:
        # Проверяем, нет ли уже заказа на этот период
        existing = BlisterOrder.objects.filter(
            user=sub.user,
            period_start__date=tomorrow.date(),
        ).exists()
        
        if not existing:
            # Создаем новый заказ
            period_end = tomorrow + timedelta(days=sub.plan.interval_days)
            
            order = BlisterOrder.objects.create(
                user=sub.user,
                subscription=sub,
                status=balirateOrder.Status.PENDING,
                period_start=tomorrow,
                period_end=period_end,
                shipping_name=sub.user.full_name,
                shipping_street=sub.user.street,
                shipping_postal_code=sub.user.postal_code,
                shipping_city=sub.user.city,
                shipping_country=sub.user.country,
            )
            
            # Копируем активные медикаменты
            for med in sub.user.medications.filter(is_active=True):
                order.items.create(
                    medication_name=med.name,
                    medication_dosage=med.dosage,
                    medication_pzn=med.pzn,
                    morning=med.morning,
                    noon=med.noon,
                    evening=med.evening,
                    night=med.night,
                    quantity=1,
                )
            
            send_order_confirmation.delay(order.id)
            created += 1
    
    logger.info(f"Created {created} scheduled orders")
    return created


# ===========================================
# CLEANUP TASKS
# ===========================================

@shared_task
def cleanup_old_documents():
    """
    Удалить старые отклоненные документы.
    Запускается еженедельно.
    """
    from accounts.models import UserDocument
    
    cutoff = timezone.now() - timedelta(days=30)
    
    old_docs = UserDocument.objects.filter(
        status=UserDocument.Status.REJECTED,
        created_at__lt=cutoff,
    )
    
    count = old_docs.count()
    
    for doc in old_docs:
        doc.file.delete()
        doc.delete()
    
    logger.info(f"Cleaned up {count} old rejected documents")
    return count


@shared_task
def cleanup_unverified_accounts():
    """
    Удалить неподтверждённые аккаунты старше 2 часов.
    Запускается каждые 30 минут.
    """
    from allauth.account.models import EmailAddress
    from accounts.models import User
    
    cutoff = timezone.now() - timedelta(hours=2)
    
    # Находим email адреса без подтверждения старше 2 часов
    unverified_emails = EmailAddress.objects.filter(
        verified=False,
        user__date_joined__lt=cutoff,
    ).exclude(
        # Исключаем Google OAuth (они автоматически подтверждены)
        user__socialaccount__isnull=False
    )
    
    # Получаем пользователей
    user_ids = unverified_emails.values_list('user_id', flat=True)
    
    # Удаляем пользователей (каскадно удалит EmailAddress)
    deleted_count, _ = User.objects.filter(
        id__in=user_ids,
        is_staff=False,  # Не удаляем staff
        subscriptions__isnull=True,  # Без подписок
    ).delete()
    
    logger.info(f"Cleaned up {deleted_count} unverified accounts")
    return deleted_count
