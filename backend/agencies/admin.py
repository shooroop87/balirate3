from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import BlisterOrder, BlisterOrderItem, Medication, Shipment


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ["name", "dosage", "user", "schedule_display", "is_active"]
    list_filter = ["is_active", "morning", "noon", "evening", "night"]
    search_fields = ["name", "pzn", "user__email"]
    raw_id_fields = ["user"]


class BlisterOrderItemInline(admin.TabularInline):
    model = BlisterOrderItem
    extra = 0
    readonly_fields = ["medication_name", "medication_dosage"]


class ShipmentInline(admin.StackedInline):
    model = Shipment
    extra = 0
    readonly_fields = ["tracking_link", "last_tracking_update", "tracking_events"]
    
    def tracking_link(self, obj):
        if obj.tracking_number:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.dhl_tracking_url,
                obj.tracking_number
            )
        return "-"
    tracking_link.short_description = _("Tracking-Link")


@admin.register(BlisterOrder)
class BlisterOrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number", "user", "status", "period_start", 
        "period_end", "shipped_at", "created_at"
    ]
    list_filter = ["status", "created_at", "shipped_at"]
    search_fields = ["order_number", "user__email", "shipping_city"]
    raw_id_fields = ["user", "subscription"]
    readonly_fields = ["order_number", "created_at", "updated_at"]
    inlines = [BlisterOrderItemInline, ShipmentInline]
    
    fieldsets = (
        (None, {"fields": ("order_number", "user", "subscription", "status")}),
        (_("Zeitraum"), {"fields": ("period_start", "period_end")}),
        (_("Lieferadresse"), {
            "fields": (
                "shipping_name", "shipping_street", 
                "shipping_postal_code", "shipping_city", "shipping_country"
            )
        }),
        (_("Notizen"), {
            "fields": ("pharmacy_notes", "customer_notes"),
            "classes": ("collapse",),
        }),
        (_("Daten"), {
            "fields": ("processed_at", "shipped_at", "delivered_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = [
        "tracking_number", "order", "carrier", "status", 
        "estimated_delivery", "created_at"
    ]
    list_filter = ["status", "carrier", "created_at"]
    search_fields = ["tracking_number", "order__order_number", "order__user__email"]
    raw_id_fields = ["order"]
    readonly_fields = ["tracking_events", "last_tracking_update"]