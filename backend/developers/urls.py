# deliveries/urls.py
from django.urls import path

from . import views

app_name = "deliveries"

urlpatterns = [
    # Публичный tracking
    path("tracking/", views.tracking_form, name="tracking_form"),
    path("tracking/<str:tracking_number>/", views.tracking_detail, name="tracking_detail"),
    
    # API для обновления (вызывается через cron/celery)
    path("api/update-tracking/<int:shipment_id>/", views.api_update_tracking, name="api_update_tracking"),
]