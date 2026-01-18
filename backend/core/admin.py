from django.contrib import admin
from .models import Video, ContactRequest, FAQ, SiteSettings


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "developer", "is_active", "created_at", "preview"]
    list_filter = ["is_active", "developer"]
    search_fields = ["title"]
    raw_id_fields = ["developer"]
    
    fieldsets = (
        (None, {
            "fields": ("title", "youtube_id", "developer", "is_active")
        }),
        ("Превью (выберите один вариант)", {
            "fields": ("thumbnail", "thumbnail_url_external"),
            "description": "Загрузите файл ИЛИ вставьте ссылку. Если оба пустые — возьмётся автоматически с YouTube."
        }),
    )
    
    def preview(self, obj):
        from django.utils.html import format_html
        return format_html('<img src="{}" width="80" height="45" style="object-fit: cover; border-radius: 4px;"/>', obj.thumbnail_url)
    preview.short_description = "Превью"


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "source", "is_processed", "created_at"]
    list_filter = ["is_processed", "source", "created_at"]
    search_fields = ["name", "phone", "email"]
    readonly_fields = ["created_at"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "order", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["order", "is_active"]
    search_fields = ["question", "answer"]
    ordering = ["order"]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("О нас", {
            "fields": ("about_title", "about_text")
        }),
        ("Контакты", {
            "fields": ("site_name", "contact_email", "contact_phone", "contact_address")
        }),
        ("Соцсети", {
            "fields": ("telegram_link", "whatsapp_link", "instagram_link", "youtube_link")
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description")
        }),
    )
    
    def has_add_permission(self, request):
        # Только одна запись
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False