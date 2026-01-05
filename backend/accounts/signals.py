# accounts/signals.py
"""
Signals для отправки уведомлений.
"""
from allauth.account.signals import email_confirmed
from django.dispatch import receiver

from core.services.sendpulse import SendPulseService


@receiver(email_confirmed)
def on_email_confirmed(request, email_address, **kwargs):
    """
    Когда пользователь подтвердил email — уведомляем админа.
    Срабатывает только для email регистрации (не Google).
    """
    user = email_address.user
    
    # Проверяем что это НЕ Google пользователь
    if not user.socialaccount_set.exists():
        SendPulseService.send_admin_new_user_notification(user)