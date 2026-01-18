from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class DeveloperCategory(models.Model):
    """Категории: Премиум, Бизнес+, Средний"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField("Иконка (URL)", max_length=500, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Категория девелоперов"
        verbose_name_plural = "Категории девелоперов"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Developer(models.Model):
    """Застройщик"""
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    
    category = models.ForeignKey(
        DeveloperCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="developers"
    )
    
    logo = models.ImageField("Логотип", upload_to="developers/logos/", blank=True)
    cover_image = models.ImageField("Обложка", upload_to="developers/covers/", blank=True)
    
    short_description = models.TextField("Краткое описание", max_length=500, blank=True)
    description = models.TextField("Полное описание (HTML)", blank=True)
    
    # Статистика
    completed_count = models.PositiveIntegerField("Сдано объектов", default=0)
    in_progress_count = models.PositiveIntegerField("Строится", default=0)
    
    # Рейтинги (1-5)
    rating = models.DecimalField("Общий рейтинг", max_digits=2, decimal_places=1, default=5.0)
    premium_rating = models.PositiveSmallIntegerField("Премиальность", default=5)
    support_rating = models.PositiveSmallIntegerField("Поддержка", default=5)
    quality_rating = models.PositiveSmallIntegerField("Качество", default=5)
    
    # Контакты
    website = models.URLField("Сайт", blank=True)
    telegram = models.CharField("Telegram", max_length=100, blank=True)
    whatsapp = models.CharField("WhatsApp", max_length=50, blank=True)
    instagram = models.CharField("Instagram", max_length=100, blank=True)
    
    is_verified = models.BooleanField("Верифицирован", default=False)
    is_active = models.BooleanField("Активен", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Застройщик"
        verbose_name_plural = "Застройщики"
        ordering = ["-rating", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("developers:detail", kwargs={"slug": self.slug})

    @property
    def total_objects(self):
        return self.completed_count + self.in_progress_count

    @property
    def reviews_count(self):
        return self.reviews.count()


class DeveloperReview(models.Model):
    """Отзыв о застройщике"""
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    
    user_name = models.CharField("Имя", max_length=100)
    user_avatar = models.ImageField("Аватар", upload_to="reviews/avatars/", blank=True)
    user_avatar_url = models.URLField("Или ссылка на аватар", max_length=500, blank=True)
    
    rating = models.PositiveSmallIntegerField("Оценка", choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField("Текст отзыва")
    
    is_approved = models.BooleanField("Одобрен", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_name} → {self.developer.name}"
    
    def get_avatar(self):
        """Возвращает URL аватара."""
        if self.user_avatar:
            return self.user_avatar.url
        return self.user_avatar_url or ''