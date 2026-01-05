from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Medication(models.Model):
    """Медикаменты пользователя для блистеров."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medications",
        verbose_name=_("Benutzer"),
    )
    
    name = models.CharField(_("Medikamentenname"), max_length=255)
    dosage = models.CharField(_("Dosierung"), max_length=100)
    pzn = models.CharField(_("PZN"), max_length=20, blank=True)  # Pharmazentralnummer
    
    # Расписание приёма
    morning = models.BooleanField(_("Morgens"), default=False)
    noon = models.BooleanField(_("Mittags"), default=False)
    evening = models.BooleanField(_("Abends"), default=False)
    night = models.BooleanField(_("Nachts"), default=False)
    
    instructions = models.TextField(_("Einnahmehinweise"), blank=True)
    
    is_active = models.BooleanField(_("Aktiv"), default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Medikament")
        verbose_name_plural = _("Medikamente")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.dosage}"

    @property
    def schedule_display(self):
        times = []
        if self.morning:
            times.append(_("Morgens"))
        if self.noon:
            times.append(_("Mittags"))
        if self.evening:
            times.append(_("Abends"))
        if self.night:
            times.append(_("Nachts"))
        return ", ".join(str(t) for t in times)


class BlisterOrder(models.Model):
    """Заказ блистеров."""

    class Status(models.TextChoices):
        PENDING = "pending", _("Ausstehend")
        PROCESSING = "processing", _("In Bearbeitung")
        PHARMACY_CHECK = "pharmacy_check", _("Apothekenprüfung")
        PACKAGING = "packaging", _("Verpackung")
        SHIPPED = "shipped", _("Versendet")
        DELIVERED = "delivered", _("Zugestellt")
        CANCELED = "canceled", _("Storniert")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="balirate_orders",
        verbose_name=_("Benutzer"),
    )
    subscription = models.ForeignKey(
        "subscriptions.Subscription",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="balirate_orders",
        verbose_name=_("Abonnement"),
    )
    
    # Номер заказа
    order_number = models.CharField(
        _("Bestellnummer"), max_length=50, unique=True, db_index=True
    )
    
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    
    # Период блистера
    period_start = models.DateField(_("Zeitraum von"))
    period_end = models.DateField(_("Zeitraum bis"))
    
    # Адрес доставки (копия на момент заказа)
    shipping_name = models.CharField(_("Empfängername"), max_length=255)
    shipping_street = models.CharField(_("Straße"), max_length=255)
    shipping_postal_code = models.CharField(_("PLZ"), max_length=10)
    shipping_city = models.CharField(_("Stadt"), max_length=100)
    shipping_country = models.CharField(_("Land"), max_length=2, default="DE")
    
    # Примечания
    pharmacy_notes = models.TextField(_("Apothekennotizen"), blank=True)
    customer_notes = models.TextField(_("Kundennotizen"), blank=True)
    
    # Даты
    processed_at = models.DateTimeField(_("Bearbeitet am"), null=True, blank=True)
    shipped_at = models.DateTimeField(_("Versendet am"), null=True, blank=True)
    delivered_at = models.DateTimeField(_("Zugestellt am"), null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Blister-Bestellung")
        verbose_name_plural = _("Blister-Bestellungen")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_number} - {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Генерируем номер заказа
            import uuid
            self.order_number = f"BL-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class BlisterOrderItem(models.Model):
    """Медикаменты в заказе блистеров."""

    order = models.ForeignKey(
        BlisterOrder,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Bestellung"),
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_items",
        verbose_name=_("Medikament"),
    )
    
    # Копия данных медикамента
    medication_name = models.CharField(_("Medikamentenname"), max_length=255)
    medication_dosage = models.CharField(_("Dosierung"), max_length=100)
    medication_pzn = models.CharField(_("PZN"), max_length=20, blank=True)
    
    # Расписание
    morning = models.BooleanField(_("Morgens"), default=False)
    noon = models.BooleanField(_("Mittags"), default=False)
    evening = models.BooleanField(_("Abends"), default=False)
    night = models.BooleanField(_("Nachts"), default=False)
    
    quantity = models.PositiveIntegerField(_("Menge"), default=1)

    class Meta:
        verbose_name = _("Bestellposition")
        verbose_name_plural = _("Bestellpositionen")

    def __str__(self):
        return f"{self.medication_name} - {self.order.order_number}"


class Shipment(models.Model):
    """Отправление DHL."""

    class Status(models.TextChoices):
        LABEL_CREATED = "label_created", _("Etikett erstellt")
        PICKED_UP = "picked_up", _("Abgeholt")
        IN_TRANSIT = "in_transit", _("Unterwegs")
        OUT_FOR_DELIVERY = "out_for_delivery", _("Zustellung läuft")
        DELIVERED = "delivered", _("Zugestellt")
        FAILED = "failed", _("Zustellung fehlgeschlagen")
        RETURNED = "returned", _("Zurückgesendet")

    order = models.OneToOneField(
        BlisterOrder,
        on_delete=models.CASCADE,
        related_name="shipment",
        verbose_name=_("Bestellung"),
    )
    
    # DHL данные
    tracking_number = models.CharField(
        _("Sendungsnummer"), max_length=50, db_index=True
    )
    carrier = models.CharField(_("Versanddienstleister"), max_length=50, default="DHL")
    
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.LABEL_CREATED,
    )
    
    # Tracking URL
    tracking_url = models.URLField(_("Tracking-URL"), blank=True)
    
    # Вес и размеры
    weight = models.DecimalField(
        _("Gewicht (kg)"), max_digits=5, decimal_places=2, null=True, blank=True
    )
    
    # Даты
    estimated_delivery = models.DateField(_("Voraussichtliche Zustellung"), null=True, blank=True)
    actual_delivery = models.DateTimeField(_("Tatsächliche Zustellung"), null=True, blank=True)
    
    # Последнее обновление от DHL
    last_tracking_update = models.DateTimeField(
        _("Letztes Tracking-Update"), null=True, blank=True
    )
    tracking_events = models.JSONField(_("Tracking-Events"), default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Sendung")
        verbose_name_plural = _("Sendungen")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tracking_number} - {self.get_status_display()}"

    @property
    def dhl_tracking_url(self):
        if self.tracking_number:
            return f"https://www.dhl.de/de/privatkunden/pakete-empfangen/verfolgen.html?piececode={self.tracking_number}"
        return ""