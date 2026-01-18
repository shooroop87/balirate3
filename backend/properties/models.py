from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class PropertyType(models.Model):
    """Типы: Вилла, Апартаменты, Таунхаус"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Тип недвижимости"
        verbose_name_plural = "Типы недвижимости"

    def __str__(self):
        return self.name


class Location(models.Model):
    """Локации: Чангу, Убуд, Семиньяк"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Property(models.Model):
    """Объект недвижимости"""
    
    class Status(models.TextChoices):
        SALE = "sale", "Продажа"
        PRESALE = "presale", "Предпродажа"
        SOLD = "sold", "Продано"

    class ConstructionStatus(models.TextChoices):
        COMPLETED = "completed", "Сдан"
        IN_PROGRESS = "in_progress", "Строится"
        PLANNED = "planned", "Планируется"

    name = models.CharField("Название", max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    
    developer = models.ForeignKey(
        "developers.Developer", on_delete=models.CASCADE,
        related_name="properties", verbose_name="Застройщик"
    )
    property_type = models.ForeignKey(
        PropertyType, on_delete=models.SET_NULL,
        null=True, related_name="properties", verbose_name="Тип"
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL,
        null=True, related_name="properties", verbose_name="Локация"
    )
    
    # Медиа
    main_image = models.ImageField("Главное фото", upload_to="properties/")
    
    # Характеристики
    price_from = models.DecimalField("Цена от ($)", max_digits=12, decimal_places=0, null=True, blank=True)
    area = models.PositiveIntegerField("Площадь (м²)", null=True, blank=True)
    rooms = models.PositiveSmallIntegerField("Комнат", null=True, blank=True)
    
    # Статусы
    status = models.CharField("Статус продажи", max_length=20, choices=Status.choices, default=Status.SALE)
    construction_status = models.CharField(
        "Статус строительства", max_length=20,
        choices=ConstructionStatus.choices, default=ConstructionStatus.IN_PROGRESS
    )
    completion_date = models.CharField("Дата сдачи", max_length=50, blank=True)  # "3 квартал 2025"
    
    # Контент
    short_description = models.TextField("Краткое описание", max_length=500, blank=True)
    description = models.TextField("Полное описание (HTML)", blank=True)
    
    # ROI
    roi_percent = models.DecimalField("ROI %", max_digits=4, decimal_places=1, null=True, blank=True)
    
    is_featured = models.BooleanField("Рекомендуемый", default=False)
    is_active = models.BooleanField("Активен", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("properties:detail", kwargs={"slug": self.slug})


class PropertyImage(models.Model):
    """Дополнительные фото объекта"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Фото", upload_to="properties/gallery/")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Фото объекта"
        verbose_name_plural = "Фото объектов"
        ordering = ["order"]