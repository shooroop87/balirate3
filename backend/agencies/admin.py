from django.contrib import admin
from .models import Agency


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ["name", "rating", "is_verified", "is_active"]
    list_filter = ["is_verified", "is_active"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "is_verified", "is_active")
        }),
        ("Медиа", {
            "fields": ("logo", "cover_image")
        }),
        ("Описание", {
            "fields": ("description",)
        }),
        ("Рейтинг", {
            "fields": ("rating",)
        }),
        ("Контакты", {
            "fields": ("website", "phone", "email", "telegram", "whatsapp", "instagram", "address")
        }),
    )