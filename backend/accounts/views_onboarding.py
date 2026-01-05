from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import User, UserDocument


class OnboardingProfileForm(forms.ModelForm):
    """Форма заполнения профиля при онбординге."""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'date_of_birth',
            'street', 'postal_code', 'city', 'country',
            'insurance_number', 'insurance_company',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required = ['first_name', 'last_name', 'phone', 'date_of_birth', 
                    'street', 'postal_code', 'city']
        for field_name in required:
            self.fields[field_name].required = True
        
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


@login_required
def onboarding_profile(request):
    """Шаг 1: Заполнение профиля."""
    user = request.user
    
    if request.method == 'POST':
        form = OnboardingProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.onboarding_step = User.OnboardingStep.DOCUMENTS
            user.save(update_fields=['onboarding_step'])
            messages.success(request, _("Profil gespeichert!"))
            return redirect('onboarding_documents')
    else:
        form = OnboardingProfileForm(instance=user)
    
    return render(request, 'account/onboarding/profile.html', {
        'form': form,
        'step': 1,
        'total_steps': 4,
    })


@login_required
def onboarding_documents(request):
    """Шаг 2: Загрузка документов."""
    user = request.user
    
    if user.onboarding_step < User.OnboardingStep.DOCUMENTS:
        return redirect('onboarding_profile')
    
    documents = user.documents.all()
    has_prescription = documents.filter(document_type='prescription').exists()
    
    if request.method == 'POST':
        if 'file' in request.FILES:
            doc_type = request.POST.get('document_type', 'prescription')
            file = request.FILES['file']
            
            UserDocument.objects.create(
                user=user,
                document_type=doc_type,
                file=file,
                original_filename=file.name,
                description=request.POST.get('description', ''),
            )
            
            send_admin_notification(user, 'new_document')
            messages.success(request, _("Dokument hochgeladen!"))
            return redirect('onboarding_documents')
        
        if 'next_step' in request.POST:
            if has_prescription:
                user.onboarding_step = User.OnboardingStep.PLAN
                user.save(update_fields=['onboarding_step'])
                return redirect('onboarding_plan')
            else:
                messages.warning(request, _("Bitte laden Sie mindestens ein Rezept hoch."))
    
    return render(request, 'account/onboarding/documents.html', {
        'documents': documents,
        'has_prescription': has_prescription,
        'step': 2,
        'total_steps': 4,
    })


def send_admin_notification(user, notification_type):
    """Отправка уведомления администратору."""
    subject = f"BlisterPerPost: Neuer Benutzer - {user.email}"
    
    if notification_type == 'new_document':
        message = f"""
Neues Dokument hochgeladen!

Benutzer: {user.full_name}
E-Mail: {user.email}
Telefon: {user.phone}

Bitte prüfen Sie die Dokumente im Admin-Panel.
        """
    else:
        message = f"Neue Aktivität von {user.email}"
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass


@login_required
def onboarding_plan(request):
    """Шаг 3: Выбор тарифа."""
    user = request.user
    
    if user.onboarding_step < User.OnboardingStep.PLAN:
        return redirect('onboarding_documents')
    
    from subscriptions.models import Plan
    plans = Plan.objects.filter(is_active=True).order_by('price')
    
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        if plan_id:
            request.session['selected_plan_id'] = plan_id
            user.onboarding_step = User.OnboardingStep.PAYMENT
            user.save(update_fields=['onboarding_step'])
            return redirect('onboarding_payment')
    
    return render(request, 'account/onboarding/plan.html', {
        'plans': plans,
        'step': 3,
        'total_steps': 4,
    })


@login_required
def onboarding_payment(request):
    """Шаг 4: Оплата через PayPal."""
    user = request.user
    
    if user.onboarding_step < User.OnboardingStep.PAYMENT:
        return redirect('onboarding_plan')
    
    from subscriptions.models import Plan
    from subscriptions.paypal_service import PayPalService
    
    plan_id = request.session.get('selected_plan_id')
    plan = None
    if plan_id:
        plan = Plan.objects.filter(id=plan_id, is_active=True).first()
    
    if not plan:
        return redirect('onboarding_plan')
    
    if request.method == 'POST':
        # Создаём PayPal подписку
        success_url = request.build_absolute_uri(reverse('onboarding_complete'))
        cancel_url = request.build_absolute_uri(reverse('onboarding_payment'))
        
        try:
            result = PayPalService.create_subscription(
                user=user,
                plan=plan,
                return_url=success_url,
                cancel_url=cancel_url,
            )
            
            if result.get("approve_url"):
                return redirect(result["approve_url"])
            else:
                messages.error(request, _("Fehler beim Erstellen der PayPal-Zahlung."))
        except Exception as e:
            messages.error(request, _("PayPal-Fehler: ") + str(e))
    
    return render(request, 'account/onboarding/payment.html', {
        'plan': plan,
        'step': 4,
        'total_steps': 4,
    })


@login_required
def onboarding_complete(request):
    """Завершение онбординга после PayPal."""
    user = request.user
    subscription_id = request.GET.get('subscription_id')
    subscription = None
    
    # Активируем подписку если есть
    if subscription_id:
        from subscriptions.models import Subscription
        from subscriptions.paypal_service import PayPalService
        
        try:
            subscription = Subscription.objects.get(
                paypal_subscription_id=subscription_id,
                user=user,
            )
            PayPalService.activate_subscription(subscription)
        except Subscription.DoesNotExist:
            pass
    
    # Если нет subscription_id, ищем последнюю подписку
    if not subscription:
        subscription = user.subscriptions.order_by('-created_at').first()
    
    user.onboarding_step = User.OnboardingStep.COMPLETED
    user.onboarding_completed = True
    user.save(update_fields=['onboarding_step', 'onboarding_completed'])
    
    # Очищаем сессию
    if 'selected_plan_id' in request.session:
        del request.session['selected_plan_id']
    
    return render(request, 'account/onboarding/complete.html', {
        'subscription': subscription,
        'step': 5,
        'total_steps': 4,
    })