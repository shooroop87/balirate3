from django.contrib import admin
from django.utils import timezone
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "posts_count"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = "Статей"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "published_at"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["title", "excerpt", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "category", "status")
        }),
        ("Контент", {
            "fields": ("excerpt", "featured_image", "featured_image_url", "content")
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",),
        }),
        ("Даты", {
            "fields": ("published_at",),
        }),
    )
    
    actions = ["publish_posts"]
    
    @admin.action(description="Опубликовать выбранные статьи")
    def publish_posts(self, request, queryset):
        now = timezone.now()
        updated = queryset.update(status=BlogPost.Status.PUBLISHED, published_at=now)
        self.message_user(request, f"{updated} статей опубликовано.")