from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import path


def index(request):
    """Главная страница."""
    return render(request, "pages/index.html")


def developer_award_2025(request):
    return render(request, 'pages/developer_award_2025.html')


def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')
