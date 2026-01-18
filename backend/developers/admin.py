from django.contrib import admin
from .models import Developer, DeveloperCategory, DeveloperReview


@admin.register(DeveloperCategory)
class DeveloperCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "rating", "completed_count", "is_verified", "is_active"]
    list_filter = ["category", "is_verified", "is_active"]
    search_fields = ["name", "short_description"]
    prepopulated_fields = {"slug": ("name",)}
    
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "category", "is_verified", "is_active")
        }),
        ("Медиа", {
            "fields": ("logo", "cover_image")
        }),
        ("Описание", {
            "fields": ("short_description", "description")
        }),
        ("Статистика", {
            "fields": ("completed_count", "in_progress_count")
        }),
        ("Рейтинги", {
            "fields": ("rating", "premium_rating", "support_rating", "quality_rating")
        }),
        ("Контакты", {
            "fields": ("website", "telegram", "whatsapp", "instagram")
        }),
    )


@admin.register(DeveloperReview)
class DeveloperReviewAdmin(admin.ModelAdmin):
    list_display = ["user_name", "developer", "rating", "is_approved", "created_at"]
    list_filter = ["is_approved", "rating", "created_at"]
    search_fields = ["user_name", "text"]
    raw_id_fields = ["developer", "user"]