# blog/admin.py
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from django import forms

from .models import BlogCategory, BlogPost


class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
    class Meta:
        model = BlogPost
        fields = '__all__'


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "posts_count"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = _("Beiträge")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    
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
        (_("Inhalt"), {
            "fields": ("excerpt", "featured_image", "image_preview_large", "content")
        }),
        (_("Tags"), {
            "fields": ("tags",),
            "classes": ("collapse",),
        }),
        (_("SEO"), {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",),
        }),
        (_("Veröffentlichung"), {
            "fields": ("published_at", "created_at", "updated_at"),
        }),
    )
    
    actions = ["publish_posts", "unpublish_posts"]
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px; object-fit: cover;"/>',
                obj.featured_image.url
            )
        return "-"
    image_preview.short_description = _("Bild")
    
    def image_preview_large(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 200px;"/>',
                obj.featured_image.url
            )
        return "-"
    image_preview_large.short_description = _("Bildvorschau")
    
    @admin.action(description=_("Ausgewählte Beiträge veröffentlichen"))
    def publish_posts(self, request, queryset):
        now = timezone.now()
        updated = queryset.update(status=BlogPost.Status.PUBLISHED, published_at=now)
        self.message_user(request, f"{updated} Beiträge veröffentlicht.")
    
    @admin.action(description=_("Ausgewählte Beiträge als Entwurf markieren"))
    def unpublish_posts(self, request, queryset):
        updated = queryset.update(status=BlogPost.Status.DRAFT)
        self.message_user(request, f"{updated} Beiträge als Entwurf markiert.")
    
    def save_model(self, request, obj, form, change):
        # Автоматически устанавливаем дату публикации
        if obj.status == BlogPost.Status.PUBLISHED and not obj.published_at:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)