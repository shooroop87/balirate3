from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from django import forms

from .models import NewsCategory, NewsPost


class NewsPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
    class Meta:
        model = NewsPost
        fields = '__all__'


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "posts_count"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = "Новостей"


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    form = NewsPostAdminForm
    
    list_display = ["title", "category", "status", "published_at", "image_preview"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["title", "excerpt", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    
    readonly_fields = ["created_at", "updated_at", "image_preview_large"]
    
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "category", "status")
        }),
        ("Контент", {
            "fields": ("excerpt", "featured_image", "featured_image_url", "image_preview_large", "content")
        }),
        ("Теги", {
            "fields": ("tags",),
            "classes": ("collapse",),
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",),
        }),
        ("Публикация", {
            "fields": ("published_at", "created_at", "updated_at"),
        }),
    )
    
    actions = ["publish_posts", "unpublish_posts"]
    
    def image_preview(self, obj):
        url = obj.get_featured_image()
        if url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px; object-fit: cover;"/>', url)
        return "-"
    image_preview.short_description = "Изображение"
    
    def image_preview_large(self, obj):
        url = obj.get_featured_image()
        if url:
            return format_html('<img src="{}" style="max-height: 200px;"/>', url)
        return "-"
    image_preview_large.short_description = "Превью"
    
    @admin.action(description="Опубликовать выбранные")
    def publish_posts(self, request, queryset):
        now = timezone.now()
        updated = queryset.update(status=NewsPost.Status.PUBLISHED, published_at=now)
        self.message_user(request, f"{updated} новостей опубликовано.")
    
    @admin.action(description="Снять с публикации")
    def unpublish_posts(self, request, queryset):
        updated = queryset.update(status=NewsPost.Status.DRAFT)
        self.message_user(request, f"{updated} новостей снято с публикации.")