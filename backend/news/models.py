from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class NewsCategory(models.Model):
    """Категории новостей."""
    
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Категория новостей"
        verbose_name_plural = "Категории новостей"
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class NewsPost(models.Model):
    """Новость."""
    
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликовано"
    
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="Категория",
    )
    
    excerpt = models.TextField(
        "Краткое описание",
        max_length=500,
        help_text="Краткое описание для превью (макс 500 символов)"
    )
    
    featured_image = models.ImageField(
        "Изображение",
        upload_to="news/%Y/%m/",
        blank=True,
        null=True,
        help_text="Рекомендуемый размер: 850x478px"
    )
    featured_image_url = models.URLField(
        "Или ссылка на изображение",
        max_length=500,
        blank=True,
        help_text="Внешняя ссылка на изображение"
    )
    
    content = models.TextField("Контент")
    
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    
    tags = models.CharField(
        "Теги",
        max_length=255,
        blank=True,
        help_text="Теги через запятую"
    )
    
    meta_title = models.CharField("Meta Title", max_length=70, blank=True)
    meta_description = models.CharField("Meta Description", max_length=160, blank=True)
    
    published_at = models.DateTimeField("Дата публикации", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-published_at", "-created_at"]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"slug": self.slug})
    
    def get_featured_image(self):
        """Возвращает URL изображения."""
        if self.featured_image:
            return self.featured_image.url
        return self.featured_image_url or ''
    
    @property
    def tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
        return []