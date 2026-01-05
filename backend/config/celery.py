# config/celery.py
"""
Celery Configuration.

Celery - система для асинхронных задач.

Запуск:
    # Worker (выполняет задачи)
    celery -A config worker -l info

    # Beat (планировщик периодических задач)
    celery -A config beat -l info

    # Flower (мониторинг, опционально)
    celery -A config flower
"""
import os

from celery import Celery
from celery.schedules import crontab

# Устанавливаем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("Balirate")

# Читаем конфигурацию из Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим tasks.py в приложениях
app.autodiscover_tasks()


# Периодические задачи (расписание)
app.conf.beat_schedule = {
    # Каждые 2 часа - обновление tracking
    "update-shipment-tracking": {
        "task": "core.tasks.update_all_active_shipments",
        "schedule": crontab(minute=0, hour="*/2"),  # Каждые 2 часа
    },
    
    # Ежедневно в 8:00 - проверка подписок
    "check-expiring-subscriptions": {
        "task": "core.tasks.check_expiring_subscriptions",
        "schedule": crontab(minute=0, hour=8),
    },
    
    # Ежедневно в 8:00 - проверка trial
    "check-trial-ending": {
        "task": "core.tasks.check_trial_ending",
        "schedule": crontab(minute=0, hour=8),
    },
    
    # Ежедневно в 6:00 - создание заказов
    "create-scheduled-orders": {
        "task": "core.tasks.create_scheduled_orders",
        "schedule": crontab(minute=0, hour=6),
    },
    
    # Еженедельно в воскресенье в 3:00 - очистка
    "cleanup-old-documents": {
        "task": "core.tasks.cleanup_old_documents",
        "schedule": crontab(minute=0, hour=3, day_of_week=0),
    },

    # Каждые 30 минут - очистка неподтверждённых аккаунтов
    "cleanup-unverified-accounts": {
        "task": "core.tasks.cleanup_unverified_accounts",
        "schedule": crontab(minute="*/30"),
    },
}

app.conf.timezone = "Europe/Berlin"


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task для тестирования."""
    print(f"Request: {self.request!r}")
