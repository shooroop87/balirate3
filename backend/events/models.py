from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Event(models.Model):
    """Мероприятие"""
    
    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Предстоящее"
        ONGOING = "ongoing", "Идёт сейчас"
        COMPLETED = "completed", "Завершено"

    title = models.CharField("Название", max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    
    image = models.ImageField("Изображение", upload_to="events/", blank=True)
    
    # Контент
    short_description = models.TextField("Краткое описание", max_length=300, blank=True)
    description = models.TextField("Полное описание (HTML)")
    
    # Время и место
    event_date = models.DateTimeField("Дата и время")
    end_date = models.DateTimeField("Дата окончания", null=True, blank=True)
    
    location_name = models.CharField("Место", max_length=100)  # "Букит, Бали"
    address = models.CharField("Полный адрес", max_length=255, blank=True)
    
    # Координаты для карты
    latitude = models.DecimalField("Широта", max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField("Долгота", max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Организатор
    organizer_name = models.CharField("Организатор", max_length=255, blank=True)
    organizer = models.ForeignKey(
        "developers.Developer", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="events",
        verbose_name="Застройщик-организатор"
    )
    
    # Регистрация
    registration_url = models.URLField("Ссылка на регистрацию", blank=True)
    
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.UPCOMING)
    is_featured = models.BooleanField("На главной", default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ["-event_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"slug": self.slug})
    
    @property
    def has_map(self):
        return self.latitude and self.longitude