from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import path
from django.core.paginator import Paginator



def index(request):
    """Главная страница."""
    return render(request, "pages/index.html")


def developer_award_2025(request):
    return render(request, 'pages/developer_award_2025.html')


def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def terms_of_use(request):
    return render(request, 'pages/terms_of_use.html')

def video_list(request):
    videos = Video.objects.select_related('developer').order_by('-created_at')
    
    # Фильтр по застройщику
    developer_slug = request.GET.get('developer')
    if developer_slug:
        videos = videos.filter(developer__slug=developer_slug)
    
    paginator = Paginator(videos, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'videos': page_obj,
        'page_obj': page_obj,
        'developers_with_videos': Developer.objects.filter(videos__isnull=False).annotate(video_count=Count('videos')).distinct(),
        'popular_videos': Video.objects.order_by('-views')[:3],
        'total_videos': Video.objects.count(),
        'current_developer': developer_slug,
    }
    return render(request, 'videos/video_list.html', context)