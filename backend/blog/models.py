from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class BlogCategory(models.Model):
    """Категории: Новости, Аналитика, Гайды"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Статья/Новость"""
    
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликовано"

    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="posts",
        verbose_name="Категория"
    )
    
    excerpt = models.TextField("Краткое описание", max_length=500)
    featured_image = models.ImageField(
        "Изображение",
        upload_to="blog/%Y/%m/",
        blank=True,
        null=True,
        help_text="Рекомендуемый размер: 832x832px"
    )
    featured_image_url = models.URLField(
        "Или ссылка на изображение",
        max_length=500,
        blank=True,
        help_text="Внешняя ссылка на изображение (если не загружаете файл)"
    )

    def get_featured_image(self):
        """Возвращает URL изображения (загруженного или внешнего)."""
        if self.featured_image:
            return self.featured_image.url
        return self.featured_image_url or ''
    content = models.TextField("Контент (HTML)")
    
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.DRAFT)
    
    meta_title = models.CharField("Meta Title", max_length=70, blank=True)
    meta_description = models.CharField("Meta Description", max_length=160, blank=True)
    
    published_at = models.DateTimeField("Дата публикации", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})