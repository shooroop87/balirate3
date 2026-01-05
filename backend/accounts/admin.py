from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserDocument, ConsentLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "full_name", "city", "is_active", "has_active_subscription", "created_at"]
    list_filter = ["is_active", "is_staff", "country", "language", "onboarding_completed", "created_at"]
    search_fields = ["email", "first_name", "last_name", "phone"]
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Persönliche Daten"), {
            "fields": ("first_name", "last_name", "phone", "date_of_birth")
        }),
        (_("Adresse"), {
            "fields": ("street", "postal_code", "city", "country")
        }),
        (_("Versicherung"), {
            "fields": ("insurance_number", "insurance_company")
        }),
        (_("Einstellungen"), {
            "fields": ("language", "marketing_consent", "data_processing_consent", 
                      "terms_accepted", "terms_accepted_at")
        }),
        (_("Onboarding"), {
            "fields": ("onboarding_step", "onboarding_completed", "documents_verified"),
        }),
        (_("Zahlungsanbieter"), {
            "fields": ("paypal_payer_id", "stripe_customer_id"),
            "classes": ("collapse",),
        }),
        (_("Berechtigungen"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            "classes": ("collapse",),
        }),
        (_("Wichtige Daten"), {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse",),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2"),
        }),
    )


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ["user", "document_type", "status", "created_at", "reviewed_at"]
    list_filter = ["document_type", "status", "created_at"]
    search_fields = ["user__email", "user__first_name", "user__last_name"]
    raw_id_fields = ["user", "reviewed_by"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(ConsentLog)
class ConsentLogAdmin(admin.ModelAdmin):
    list_display = [
        "user", "consent_type", "granted", "is_active_display",
        "consent_version", "ip_address", "created_at", "withdrawn_at"
    ]
    list_filter = ["consent_type", "granted", "consent_version", "created_at"]
    search_fields = ["user__email", "ip_address"]
    readonly_fields = [
        "user", "consent_type", "granted", "consent_version",
        "ip_address", "user_agent", "consent_text_hash",
        "created_at", "withdrawn_at"
    ]
    date_hierarchy = "created_at"
    
    def is_active_display(self, obj):
        return obj.is_active
    is_active_display.boolean = True
    is_active_display.short_description = _("Aktiv")
    
    def has_add_permission(self, request):
        return False  # Только через код
    
    def has_change_permission(self, request, obj=None):
        return False  # Нельзя редактировать
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Superuser может удалять