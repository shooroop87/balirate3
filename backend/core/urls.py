from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Главная
    path("", views.index, name="index"),
    
    # Информационные страницы
    path("kontakt/", views.contact, name="contact"),
    
    # Правовые страницы
    path("datenschutz/", TemplateView.as_view(template_name="pages/privacy.html"), name="privacy"),
    path("agb/", TemplateView.as_view(template_name="pages/terms.html"), name="terms"),
    path("impressum/", TemplateView.as_view(template_name="pages/imprint.html"), name="imprint"),
    path("widerruf/", TemplateView.as_view(template_name="pages/withdrawal.html"), name="withdrawal"),
    path("einwilligung/", TemplateView.as_view(template_name="pages/consent.html"), name="consent"),
    path("cookies/", TemplateView.as_view(template_name="pages/cookies.html"), name="cookies"),
    
    # Dashboard (требует авторизации)
    path("dashboard/", views.dashboard, name="dashboard"),

    path("bewertung/", views.submit_review, name="submit_review"),
]