# blog/models.py
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class BlogCategory(models.Model):
    """Категории блога."""
    
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Blog-Kategorie")
        verbose_name_plural = _("Blog-Kategorien")
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Блог-пост."""
    
    class Status(models.TextChoices):
        DRAFT = "draft", _("Entwurf")
        PUBLISHED = "published", _("Veröffentlicht")
    
    title = models.CharField(_("Titel"), max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name=_("Kategorie"),
    )
    
    # Превью
    excerpt = models.TextField(
        _("Kurzbeschreibung"),
        max_length=500,
        help_text=_("Kurze Beschreibung für Vorschau (max 500 Zeichen)")
    )
    featured_image = models.ImageField(
        _("Beitragsbild"),
        upload_to="blog/%Y/%m/",
        help_text=_("Empfohlen: 832x832px")
    )
    
    # Контент (TinyMCE)
    content = models.TextField(_("Inhalt"))
    
    # Мета
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    
    # Теги (простая реализация через CharField)
    tags = models.CharField(
        _("Tags"),
        max_length=255,
        blank=True,
        help_text=_("Kommagetrennte Tags, z.B.: Medikamente, Gesundheit, Tipps")
    )
    
    # SEO
    meta_title = models.CharField(_("Meta-Titel"), max_length=70, blank=True)
    meta_description = models.CharField(_("Meta-Beschreibung"), max_length=160, blank=True)
    
    # Даты
    published_at = models.DateTimeField(_("Veröffentlicht am"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Blog-Beitrag")
        verbose_name_plural = _("Blog-Beiträge")
        ordering = ["-published_at", "-created_at"]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})
    
    @property
    def tags_list(self):
        """Возвращает список тегов."""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
        return []