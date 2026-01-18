from django.shortcuts import render, get_object_or_404
from .models import Event


def event_list(request):
    events = Event.objects.all()
    
    status = request.GET.get('status')
    if status:
        events = events.filter(status=status)
    
    upcoming = events.filter(status='upcoming')
    completed = events.filter(status='completed')
    
    return render(request, 'events/event_list.html', {
        'events': events,
        'upcoming_events': upcoming,
        'completed_events': completed,
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related = Event.objects.filter(status='upcoming').exclude(pk=event.pk)[:3]
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'related_events': related,
    })