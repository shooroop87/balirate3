# ...existing code...
import os
from pathlib import Path

from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Устанавливает переменную окружения, указывающую на модуль настроек Django.
# Если переменная уже задана в окружении (например, на хостинге), значение не изменится.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# BASE_DIR — корневая директория проекта (папка, на два уровня выше этого файла).
BASE_DIR = Path(__file__).resolve().parent.parent

# Создаёт и возвращает объект WSGI-приложения, который используют WSGI-серверы
# (например, gunicorn, uWSGI) для обработки HTTP-запросов в Django.
application = get_wsgi_application()
# ...existing code...