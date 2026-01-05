from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Главная
    path("", views.index, name="index"),
]