from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from deliveries.models import BlisterOrder, Medication
from subscriptions.models import Payment, PaymentMethod, Subscription

from .forms import (
    AddressForm,
    DocumentUploadForm,
    MedicationForm,
    ProfileForm,
)
from .models import User, UserDocument


# ===========================================
# PROFILE
# ===========================================

@login_required
def profile(request):
    """Профиль пользователя."""
    return render(request, "account/profile.html", {"user": request.user})


@login_required
def profile_edit(request):
    """Редактирование профиля."""
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profil erfolgreich aktualisiert."))
            return redirect("account_profile")
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, "account/profile_edit.html", {"form": form})


@login_required
def address_edit(request):
    """Редактирование адреса доставки."""
    if request.method == "POST":
        form = AddressForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Adresse erfolgreich aktualisiert."))
            return redirect("account_profile")
    else:
        form = AddressForm(instance=request.user)
    
    return render(request, "account/address_edit.html", {"form": form})


@login_required
def account_delete(request):
    """Удаление аккаунта."""
    if request.method == "POST":
        user = request.user
        logout(request)
        user.is_active = False
        user.save()
        messages.success(request, _("Ihr Konto wurde deaktiviert."))
        return redirect("index")
    
    return render(request, "account/account_delete.html")


# ===========================================
# DOCUMENTS
# ===========================================

@login_required
def documents_list(request):
    """Список документов пользователя."""
    documents = request.user.documents.all().order_by("-created_at")
    return render(request, "account/documents_list.html", {"documents": documents})


@login_required
def document_upload(request):
    """Загрузка документа."""
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.original_filename = request.FILES["file"].name
            doc.save()
            messages.success(request, _("Dokument erfolgreich hochgeladen."))
            return redirect("account_documents")
    else:
        form = DocumentUploadForm()
    
    return render(request, "account/document_upload.html", {"form": form})


@login_required
@require_POST
def document_delete(request, pk):
    """Удаление документа."""
    doc = get_object_or_404(UserDocument, pk=pk, user=request.user)
    doc.file.delete()
    doc.delete()
    messages.success(request, _("Dokument gelöscht."))
    return redirect("account_documents")


# ===========================================
# SUBSCRIPTIONS
# ===========================================

@login_required
def subscription_detail(request):
    """Детали подписки."""
    subscription = request.user.subscriptions.filter(
        status__in=["active", "trialing", "past_due", "paused"]
    ).first()
    
    from subscriptions.models import Plan
    plans = Plan.objects.filter(is_active=True).order_by("price")
    
    return render(request, "account/subscription.html", {
        "subscription": subscription,
        "plans": plans,
    })


@login_required
def subscription_change(request):
    """Изменение тарифа."""
    subscription = get_object_or_404(
        Subscription, user=request.user, status__in=["active", "trialing"]
    )
    
    from subscriptions.models import Plan
    plans = Plan.objects.filter(is_active=True).order_by("price")
    
    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        new_plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
        
        # Stripe subscription update
        subscription.plan = new_plan
        subscription.save()
        
        messages.success(request, _("Tarif erfolgreich geändert."))
        return redirect("subscriptions")
    
    return render(request, "account/subscription_change.html", {
        "subscription": subscription,
        "plans": plans,
    })


@login_required
def subscription_pause(request):
    """Пауза подписки."""
    subscription = get_object_or_404(
        Subscription, user=request.user, status="active"
    )
    
    if request.method == "POST":
        # Stripe subscription pause
        subscription.status = "paused"
        subscription.save()
        messages.success(request, _("Abonnement pausiert."))
        return redirect("subscriptions")
    
    return render(request, "account/subscription_pause.html", {
        "subscription": subscription,
    })


@login_required
def subscription_cancel(request):
    """Отмена подписки."""
    subscription = get_object_or_404(
        Subscription, user=request.user, status__in=["active", "trialing", "paused"]
    )
    
    if request.method == "POST":
        # subscription cancel
        subscription.cancel_at_period_end = True
        subscription.canceled_at = timezone.now()
        subscription.save()
        messages.success(request, _("Abonnement wird zum Ende der Periode gekündigt."))
        return redirect("subscriptions")
    
    return render(request, "account/subscription_cancel.html", {
        "subscription": subscription,
    })


# ===========================================
# PAYMENTS
# ===========================================

@login_required
def payments_list(request):
    """История платежей."""
    payments = request.user.payments.all().order_by("-created_at")
    return render(request, "account/payments_list.html", {"payments": payments})


@login_required
def payment_methods(request):
    """Методы оплаты."""
    methods = request.user.payment_methods.all().order_by("-is_default", "-created_at")
    return render(request, "account/payment_methods.html", {"methods": methods})


@login_required
def payment_method_add(request):
    """Информация о способе оплаты PayPal."""
    # Получаем активную подписку
    active_subscription = request.user.subscriptions.filter(
        status__in=["active", "trialing"]
    ).first()
    
    # Получаем PayPal метод оплаты
    paypal_method = request.user.payment_methods.filter(
        type="paypal"
    ).first()
    
    return render(request, "account/payment_method_add.html", {
        "subscription": active_subscription,
        "paypal_method": paypal_method,
    })


@login_required
@require_POST
def payment_method_delete(request, pk):
    """Удаление метода оплаты."""
    method = get_object_or_404(PaymentMethod, pk=pk, user=request.user)
    
    # Проверяем, что это не единственный метод
    if request.user.payment_methods.count() <= 1:
        messages.error(request, _("Sie müssen mindestens eine Zahlungsmethode haben."))
        return redirect("account_payment_methods")
    
    # Stripe detach payment method
    method.delete()
    messages.success(request, _("Zahlungsmethode gelöscht."))
    return redirect("account_payment_methods")


# ===========================================
# MEDICATIONS
# ===========================================

@login_required
def medications_list(request):
    """Список медикаментов."""
    medications = request.user.medications.all().order_by("name")
    return render(request, "account/medications_list.html", {"medications": medications})


@login_required
def medication_add(request):
    """Добавление медикамента."""
    if request.method == "POST":
        form = MedicationForm(request.POST)
        if form.is_valid():
            med = form.save(commit=False)
            med.user = request.user
            med.save()
            messages.success(request, _("Medikament hinzugefügt."))
            return redirect("account_medications")
    else:
        form = MedicationForm()
    
    return render(request, "account/medication_form.html", {"form": form})


@login_required
def medication_edit(request, pk):
    """Редактирование медикамента."""
    med = get_object_or_404(Medication, pk=pk, user=request.user)
    
    if request.method == "POST":
        form = MedicationForm(request.POST, instance=med)
        if form.is_valid():
            form.save()
            messages.success(request, _("Medikament aktualisiert."))
            return redirect("account_medications")
    else:
        form = MedicationForm(instance=med)
    
    return render(request, "account/medication_form.html", {"form": form, "medication": med})


@login_required
@require_POST
def medication_delete(request, pk):
    """Удаление медикамента."""
    med = get_object_or_404(Medication, pk=pk, user=request.user)
    med.is_active = False
    med.save()
    messages.success(request, _("Medikament deaktiviert."))
    return redirect("account_medications")


# ===========================================
# ORDERS
# ===========================================

@login_required
def orders_list(request):
    """Список заказов."""
    orders = request.user.balirate_orders.all().order_by("-created_at")
    return render(request, "account/orders_list.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    """Детали заказа."""
    order = get_object_or_404(BlisterOrder, order_number=order_number, user=request.user)
    return render(request, "account/order_detail.html", {"order": order})