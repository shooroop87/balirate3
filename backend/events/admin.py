from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "event_date", "location_name", "status", "is_featured"]
    list_filter = ["status", "is_featured", "event_date"]
    search_fields = ["title", "description", "location_name"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "event_date"
    
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "status", "is_featured")
        }),
        ("Контент", {
            "fields": ("image", "short_description", "description")
        }),
        ("Время и место", {
            "fields": ("event_date", "end_date", "location_name", "address", "latitude", "longitude")
        }),
        ("Организатор", {
            "fields": ("organizer_name", "organizer", "registration_url")
        }),
    )