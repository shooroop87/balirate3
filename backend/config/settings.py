# config/settings.py - ИСПРАВЛЕНА СТРУКТУРА ШАБЛОНОВ
import io
import os
import sys
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "1insecure1-1default1")

# DEBUG
DEBUG = True

# ALLOWED_HOSTS
if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost 127.0.0.1 217.154.149.73 parisweek.ru www.parisweek.ru").split()

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://localhost:10000",
    "http://127.0.0.1:10000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://parisweek.ru",
    "https://www.parisweek.ru",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ===========================================
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    
    # 3rd party - Auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    
    # 3rd party - Other
    "parler",
    "taggit",
    "meta",
    "tinymce",
    "easy_thumbnails",
    "filer",
    "mptt",
    "crispy_forms",
    "crispy_bootstrap5",
    
    # Local apps
    "accounts",
    "core",
    "developers",
    "properties",
    "agencies",
    "blog",
    "events",
    "news",
]

SITE_ID = 1

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Auth
AUTH_USER_MODEL = 'accounts.User'

# Thumbnails
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "easy_thumbnails.processors.scale_and_crop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

SITE_ID = 1

# Dev-only apps
if DEBUG:
    INSTALLED_APPS += [
        "django_browser_reload",
    ]

# ===========================================
# MIDDLEWARE
# ===========================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

ROOT_URLCONF = "config.urls"

TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "core" / "templates",
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ===========================================
# DATABASE
# ===========================================
if os.getenv("DATABASE_URL"):
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
    }
elif os.getenv("USE_SQLITE", "0") == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "balirate"),
            "USER": os.getenv("POSTGRES_USER", "balirate_user"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "balirate_password"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5450"),
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Локальная разработка
if not os.environ.get('DOCKER_ENV') and any(cmd in sys.argv for cmd in ['runserver', 'migrate', 'makemigrations', 'shell', 'createsuperuser']):
    DATABASES['default']['HOST'] = 'localhost'

# Cache (Redis)
if os.environ.get('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# ===========================================
# AUTHENTICATION
# ===========================================
AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# ===========================================
# ALLAUTH - Custom User без username
# ===========================================
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "first_name*", "last_name*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""

# Для email ссылок
if DEBUG:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
else:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/account/login/"

# Google OAuth
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
        },
    }
}

# ===========================================
# SENDPULSE
# ===========================================
SENDPULSE_API_USER_ID = os.getenv("SENDPULSE_API_USER_ID", "")
SENDPULSE_API_SECRET = os.getenv("SENDPULSE_API_SECRET", "")
SENDPULSE_FROM_EMAIL = os.getenv("SENDPULSE_FROM_EMAIL", "noreply@parisweek.ru")
SENDPULSE_FROM_NAME = os.getenv("SENDPULSE_FROM_NAME", "Balirate")


# Social auth
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

# Custom Adapter для HTML emails
#ACCOUNT_ADAPTER = 'accounts.adapters.HTMLEmailAccountAdapter'

# Custom signup form с DSGVO согласиями
#ACCOUNT_FORMS = {
#    "signup": "accounts.forms.CustomSignupForm",
#}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

#ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
#ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/dashboard/"

# ===========================================
# INTERNATIONALIZATION (DE primary, EN secondary)
# ===========================================
LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Makassar"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

PARLER_LANGUAGES = {
    SITE_ID: (
        {"code": "ru", "fallbacks": ["en"], "hide_untranslated": False},
        {"code": "en", "fallbacks": ["ru"], "hide_untranslated": False},
    ),
    "default": {
        "fallbacks": ['ru'],
        "hide_untranslated": False,
    },
}


# ===========================================
# STATIC & MEDIA
# ===========================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "collected_static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

FILE_UPLOAD_PERMISSIONS = 0o644  # rw-r--r--
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755  # rwxr-xr-x

# Создаем медиа-директорию
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Filer / thumbnails
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_QUALITY = 90
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "easy_thumbnails.processors.scale_and_crop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

# ===========================================
# EMAIL
# ===========================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.ionos.de")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "Balirate <service@parisweek.ru>")


# ===========================================
# CELERY
# ===========================================
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# ===========================================
# THUMBNAILS (Filer)
# ===========================================
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_QUALITY = 90
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "easy_thumbnails.processors.scale_and_crop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

# ===========================================
# SECURITY (Production only)
# ===========================================
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ===========================================
# LOGGING
# ===========================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

# ===================== DJANGO TINYMCE =====================
BLEACH_ALLOWED_TAGS = [
    'i', 'span',
]

BLEACH_ALLOWED_ATTRIBUTES = {
    '*': ['class', 'style', 'title', 'aria-label'],
    'i': ['class', 'style', 'data-*'],
    'span': ['class', 'style', 'data-*'],
}

BLEACH_STRIP = False

# Базовые настройки TinyMCE
# TINYMCE_API_KEY = 'f80axcxfwy4juoux11elmrxusxzpkbrz85w43nyvug2yta1a'
# TINYMCE_JS_URL = f"https://cdn.tiny.cloud/1/{TINYMCE_API_KEY}/tinymce/6/tinymce.min.js"
TINYMCE_JS_URL = "/static/tinymce/tinymce.min.js"
TINYMCE_COMPRESSOR = False
TINYMCE_SPELLCHECKER = False

# Основная конфигурация (аналог CKEditor 5 'default')
TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "width": "auto",
    "menubar": "file edit view insert format tools table",
    "plugins": """
        advlist autolink lists link image charmap preview anchor searchreplace 
        visualblocks code fullscreen insertdatetime media table paste code 
        help wordcount imagetools table lists emoticons codesample nonbreaking pagebreak
    """,
    "toolbar": """
        undo redo | styles | bold italic underline strikethrough | 
        forecolor backcolor | alignleft aligncenter alignright alignjustify |
        bullist numlist outdent indent | link image media swipergallery | 
        table | removeformat code fullscreen help
    """,
    "external_plugins": {
        "swipergallery": "/static/tinymce/plugins/swipergallery/plugin.js"
    },
    # Стили для заголовков (аналог heading в CKEditor)
    "style_formats": [
        {"title": "Paragraph", "format": "p", "classes": "mt-20"},
        {"title": "Heading 1", "format": "h1"},
        {"title": "Heading 2", "format": "h2", "classes": "text-30 md:text-24"},
        {"title": "Heading 3", "format": "h3"},
        {"title": "Heading 4", "format": "h4"},
        {"title": "Heading 5", "format": "h5"},
        {"title": "Heading 6", "format": "h6"},
        {
            "title": "CTA Button",
            "selector": "a",
            "classes": "cta-button button -md -dark-1 bg-accent-1 text-white",
        },
        {
            "title": "CTA Outline",
            "selector": "a",
            "classes": "cta-button-outline button -outline-accent-1 text-accent-1",
        },
    ],
    # Цвета (аналог fontColor в CKEditor)
    "color_map": [
        "000000",
        "Black",
        "4D4D4D",
        "Dark grey",
        "999999",
        "Grey",
        "E6E6E6",
        "Light grey",
        "FFFFFF",
        "White",
        "E64C4C",
        "Red",
        "E6804C",
        "Orange",
        "E6E64C",
        "Yellow",
        "99E64C",
        "Light green",
        "4CE64C",
        "Green",
        "4CE699",
        "Aquamarine",
        "4CE6E6",
        "Turquoise",
        "4C99E6",
        "Light blue",
        "4C4CE6",
        "Blue",
        "994CE6",
        "Purple",
        "E64CE6",
        "Magenta",
        "E64C99",
        "Pink",
    ],
    # Настройки изображений (аналог image в CKEditor)
    "image_advtab": True,
    "image_caption": True,
    "image_title": True,
    "automatic_uploads": True,
    "file_picker_types": "image",
    "images_upload_url": "/tinymce/upload/",
    "images_reuse_filename": False,
    # Таблицы (аналог table в CKEditor)
    "table_toolbar": "tableprops tabledelete | tableinsertrowbefore tableinsertrowafter tabledeleterow | tableinsertcolbefore tableinsertcolafter tabledeletecol",
    "table_appearance_options": True,
    "table_grid": True,
    "table_resize_bars": True,
    "table_default_attributes": {"border": "1"},
    "table_default_styles": {"border-collapse": "collapse", "width": "100%"},
    # Контент CSS (стили как в CKEditor)
    "content_css": "/static/css/ckeditor-content.css",
    "content_style": """
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #32373c;
            padding: 20px;
        }
    """,
    # Разрешенные элементы
    "extended_valid_elements": """
        div[class|style|data-*],
        span[class|style|data-*],
        i[class|style|data-*],
        span[class|style|data-*],
        img[class|src|alt|title|width|height|loading|data-*],
        a[href|target|rel|class|style],
        iframe[src|width|height|frameborder|allow|allowfullscreen|title|loading|referrerpolicy],
        figure[class|data-*],
        table[class|style|border|cellpadding|cellspacing],
        td[class|style|colspan|rowspan|data-label],
        th[class|style|colspan|rowspan|data-label]
    """,
    "valid_classes": {
        "div": "table-responsive,table-stack,stack-item,image-gallery,gallery-grid,gallery-item,media",
        "img": "gallery-image",
        "table": "compact,striped,lake-como-table,table-normal",
        "span": "stack-label,stack-value,stack-header",
        "h2": "text-30,md:text-24",
        "p": "mt-20",
        "ul": "list-disc,mt-20",
        "ol": "numbered-list,mt-20",
    },
    # Опции
    "branding": False,
    "promotion": False,
    "relative_urls": False,
    "remove_script_host": False,
    "convert_urls": True,
    "cleanup": True,
    "cleanup_on_startup": True,
    "paste_as_text": False,
    "paste_data_images": True,
    "browser_spellcheck": True,
    "contextmenu": "link image table",
}


# Настройки загрузки файлов (аналог CKEDITOR_5_UPLOAD_PATH)
TINYMCE_UPLOAD_PATH = "blog/content/"
TINYMCE_IMAGE_UPLOAD_ENABLED = True
TINYMCE_FILE_UPLOAD_ENABLED = True
TINYMCE_ALLOWED_FILE_TYPES = ["jpeg", "jpg", "png", "gif", "webp", "pdf", "doc", "docx"]


# Теги / изображения / пагинация
TAGGIT_CASE_INSENSITIVE = True

THUMBNAIL_FORMAT = "WEBP"
THUMBNAIL_QUALITY = 85
THUMBNAIL_PRESERVE_FORMAT = False

PAGINATE_BY = 10

FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024  # 15MB

ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

IMAGE_QUALITY = 85
MAX_IMAGE_WIDTH = 1200
MAX_IMAGE_HEIGHT = 1200

THUMBNAIL_ALIASES = {
    "": {
        # Hero и слайдеры главной
        "hero_mobile": {"size": (640, 360), "crop": "smart", "quality": 80, "format": "WEBP"},
        "hero_tablet": {"size": (1024, 576), "crop": "smart", "quality": 85, "format": "WEBP"},
        "hero_desktop": {"size": (1920, 1080), "crop": "smart", "quality": 90, "format": "WEBP"},
        
        # Карточки туров
        "tour_card_mobile": {"size": (400, 280), "crop": "smart", "quality": 80, "format": "WEBP"},
        "tour_card_tablet": {"size": (600, 420), "crop": "smart", "quality": 85, "format": "WEBP"},
        "tour_card_desktop": {"size": (800, 560), "crop": "smart", "quality": 90, "format": "WEBP"},
        
        # Детальная страница тура (галерея)
        "tour_gallery_mobile": {"size": (480, 320), "crop": "smart", "quality": 80, "format": "WEBP"},
        "tour_gallery_tablet": {"size": (768, 512), "crop": "smart", "quality": 85, "format": "WEBP"},
        "tour_gallery_desktop": {"size": (1200, 800), "crop": "smart", "quality": 90, "format": "WEBP"},
        
        # Блог - карточки
        "blog_card_mobile": {"size": (400, 300), "crop": "smart", "quality": 80, "format": "WEBP"},
        "blog_card_tablet": {"size": (600, 450), "crop": "smart", "quality": 85, "format": "WEBP"},
        "blog_card_desktop": {"size": (800, 600), "crop": "smart", "quality": 90, "format": "WEBP"},
        
        # Блог - детальная страница
        "blog_hero_mobile": {"size": (640, 400), "crop": "smart", "quality": 80, "format": "WEBP"},
        "blog_hero_tablet": {"size": (1024, 640), "crop": "smart", "quality": 85, "format": "WEBP"},
        "blog_hero_desktop": {"size": (1920, 1200), "crop": "smart", "quality": 90, "format": "WEBP"},
        
        # Команда (About page)
        "team_mobile": {"size": (480, 480), "crop": "smart", "quality": 80, "format": "WEBP"},
        "team_tablet": {"size": (768, 768), "crop": "smart", "quality": 85, "format": "WEBP"},
        "team_desktop": {"size": (1024, 1024), "crop": "smart", "quality": 90, "format": "WEBP"},
        
        # Отзывы (Reviews)
        "review_thumb": {"size": (60, 60), "crop": "smart", "quality": 85, "format": "WEBP"},
        "review_avatar": {"size": (100, 100), "crop": "smart", "quality": 85, "format": "WEBP"},
        
        # Миниатюры для виджетов
        "widget_thumb": {"size": (80, 80), "crop": "smart", "quality": 80, "format": "WEBP"},
        
        # OG Image для соцсетей
        "og_image": {"size": (1200, 630), "crop": "smart", "quality": 90, "format": "JPEG"},
    }
}
