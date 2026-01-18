from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Event


def event_list(request):
    """Список мероприятий"""
    sort = request.GET.get('sort', 'upcoming')
    
    now = timezone.now()
    
    if sort == 'past':
        # Прошедшие
        events = Event.objects.filter(event_date__lt=now).order_by('-event_date')
        active_tab = 'past'
    else:
        # Предстоящие
        events = Event.objects.filter(event_date__gte=now).order_by('event_date')
        active_tab = 'upcoming'
    
    paginator = Paginator(events, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'events/event_list.html', {
        'events': page_obj,
        'page_obj': page_obj,
        'active_tab': active_tab,
    })


def event_detail(request, slug):
    """Детальная страница мероприятия"""
    event = get_object_or_404(Event, slug=slug)
    related = Event.objects.filter(status='upcoming').exclude(pk=event.pk)[:3]
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'related_events': related,
    })