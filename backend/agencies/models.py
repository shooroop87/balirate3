from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Agency(models.Model):
    """Агентство недвижимости"""
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    
    logo = models.ImageField("Логотип", upload_to="agencies/logos/", blank=True)
    cover_image = models.ImageField("Обложка", upload_to="agencies/covers/", blank=True)
    
    description = models.TextField("Описание", blank=True)
    
    # Контакты
    website = models.URLField("Сайт", blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    telegram = models.CharField("Telegram", max_length=100, blank=True)
    whatsapp = models.CharField("WhatsApp", max_length=50, blank=True)
    instagram = models.CharField("Instagram", max_length=100, blank=True)
    
    address = models.CharField("Адрес", max_length=255, blank=True)
    
    rating = models.DecimalField("Рейтинг", max_digits=2, decimal_places=1, default=5.0)
    is_verified = models.BooleanField("Верифицировано", default=False)
    is_active = models.BooleanField("Активно", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Агентство"
        verbose_name_plural = "Агентства"
        ordering = ["-rating", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("agencies:detail", kwargs={"slug": self.slug})