from django.db import models


class Video(models.Model):
    """Видео от застройщиков"""
    title = models.CharField("Название", max_length=255)
    youtube_id = models.CharField(
        "YouTube ID", 
        max_length=20,
        help_text="ID из ссылки YouTube. Пример: для https://www.youtube.com/watch?v=W7uANluGQSY&t=2s введите: W7uANluGQSY"
    )
    
    developer = models.ForeignKey(
        "developers.Developer", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="videos",
        verbose_name="Застройщик"
    )
    
    # Превью - либо файл, либо URL
    thumbnail = models.ImageField("Превью (файл)", upload_to="videos/", blank=True)
    thumbnail_url_external = models.URLField(
        "Превью (ссылка)", 
        blank=True,
        help_text="Или вставьте ссылку на изображение. Пример: https://img.youtube.com/vi/W7uANluGQSY/maxresdefault.jpg"
    )
    
    views = models.PositiveIntegerField("Просмотры", default=0)
    is_active = models.BooleanField("Активно", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def youtube_url(self):
        return f"https://www.youtube.com/watch?v={self.youtube_id}"

    @property
    def thumbnail_url(self):
        # Приоритет: загруженный файл > внешняя ссылка > автоматическая от YouTube
        if self.thumbnail:
            return self.thumbnail.url
        if self.thumbnail_url_external:
            return self.thumbnail_url_external
        return f"https://img.youtube.com/vi/{self.youtube_id}/maxresdefault.jpg"


class ContactRequest(models.Model):
    """Заявки на консультацию"""
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    telegram = models.CharField("Telegram", max_length=100, blank=True)
    
    message = models.TextField("Сообщение", blank=True)
    source = models.CharField("Источник", max_length=100, blank=True)
    
    is_processed = models.BooleanField("Обработано", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.created_at:%d.%m.%Y}"


class FAQ(models.Model):
    """Вопросы и ответы"""
    question = models.CharField("Вопрос", max_length=500)
    answer = models.TextField("Ответ")
    
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Вопрос-ответ"
        verbose_name_plural = "Вопросы и ответы"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.question[:50]
    

class SiteSettings(models.Model):
    """Настройки сайта (singleton)"""
    
    # О нас
    about_title = models.CharField("Заголовок секции О нас", max_length=200, default="О нас")
    about_text = models.TextField("Текст О нас (HTML)", blank=True)
    
    # Контакты
    site_name = models.CharField("Название сайта", max_length=100, default="Balirate")
    contact_email = models.EmailField("Email", default="info@balirate.com")
    contact_phone = models.CharField("Телефон", max_length=50, blank=True)
    contact_address = models.CharField("Адрес", max_length=255, default="Бали, Индонезия")
    
    # Соцсети
    telegram_link = models.URLField("Telegram", default="https://t.me/balirate", blank=True)
    whatsapp_link = models.URLField("WhatsApp", blank=True)
    instagram_link = models.URLField("Instagram", blank=True)
    youtube_link = models.URLField("YouTube", blank=True)
    
    # SEO
    meta_title = models.CharField("Meta Title главной", max_length=70, default="Balirate - Рейтинг застройщиков Бали")
    meta_description = models.CharField("Meta Description главной", max_length=160, default="Независимый рейтинг застройщиков на Бали")
    
    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj