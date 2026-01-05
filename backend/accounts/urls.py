# accounts/urls.py
from django.urls import path

from . import views
from . import views_onboarding

urlpatterns = [
    # Onboarding (должен быть первым!)
    path("onboarding/", views_onboarding.onboarding_profile, name="onboarding_profile"),
    path("onboarding/profile/", views_onboarding.onboarding_profile, name="onboarding_profile_alt"),
    path("onboarding/documents/", views_onboarding.onboarding_documents, name="onboarding_documents"),
    path("onboarding/plan/", views_onboarding.onboarding_plan, name="onboarding_plan"),
    path("onboarding/payment/", views_onboarding.onboarding_payment, name="onboarding_payment"),
    path("onboarding/complete/", views_onboarding.onboarding_complete, name="onboarding_complete"),
    
    # Profile
    path("profile/", views.profile, name="account_profile"),
    path("profile/edit/", views.profile_edit, name="account_profile_edit"),
    path("address/", views.address_edit, name="account_address"),
    path("delete/", views.account_delete, name="account_delete"),
    
    # Documents
    path("documents/", views.documents_list, name="account_documents"),
    path("documents/upload/", views.document_upload, name="account_document_upload"),
    path("documents/<int:pk>/delete/", views.document_delete, name="account_document_delete"),
    
    # Subscriptions
    path("subscription/", views.subscription_detail, name="subscriptions"),
    path("subscription/change/", views.subscription_change, name="subscription_change"),
    path("subscription/pause/", views.subscription_pause, name="subscription_pause"),
    path("subscription/cancel/", views.subscription_cancel, name="subscription_cancel"),
    
    # Payments
    path("payments/", views.payments_list, name="account_payments"),
    path("payment-methods/", views.payment_methods, name="account_payment_methods"),
    path("payment-methods/add/", views.payment_method_add, name="account_payment_method_add"),
    path("payment-methods/<int:pk>/delete/", views.payment_method_delete, name="account_payment_method_delete"),
    
    # Medications
    path("medications/", views.medications_list, name="account_medications"),
    path("medications/add/", views.medication_add, name="account_medication_add"),
    path("medications/<int:pk>/edit/", views.medication_edit, name="account_medication_edit"),
    path("medications/<int:pk>/delete/", views.medication_delete, name="account_medication_delete"),
    
    # Orders
    path("orders/", views.orders_list, name="account_orders"),
    path("orders/<str:order_number>/", views.order_detail, name="account_order_detail"),
]