from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Главная
    path("", views.index, name="index"),
    path('developer-award-2025/', views.developer_award_2025, name='developer_award_2025'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
    path('contact/', views.contact_request, name='contact_request'),
]
