from django.shortcuts import render, get_object_or_404
from .models import Agency


def agency_list(request):
    agencies = Agency.objects.filter(is_active=True)
    return render(request, 'agencies/agency_list.html', {
        'agencies': agencies,
    })


def agency_detail(request, slug):
    agency = get_object_or_404(Agency, slug=slug, is_active=True)
    return render(request, 'agencies/agency_detail.html', {
        'agency': agency,
    })