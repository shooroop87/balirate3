from django.contrib import admin
from .models import Property, PropertyType, Location, PropertyImage


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["name", "developer", "property_type", "location", "price_from", "status", "is_featured"]
    list_filter = ["status", "construction_status", "property_type", "location", "is_featured"]
    search_fields = ["name", "short_description"]
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ["developer"]
    inlines = [PropertyImageInline]
    
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "developer", "property_type", "location")
        }),
        ("Медиа", {
            "fields": ("main_image",)
        }),
        ("Характеристики", {
            "fields": ("price_from", "area", "rooms", "roi_percent")
        }),
        ("Статусы", {
            "fields": ("status", "construction_status", "completion_date", "is_featured", "is_active")
        }),
        ("Описание", {
            "fields": ("short_description", "description")
        }),
    )