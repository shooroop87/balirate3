from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Property, PropertyType, Location


def property_list(request):
    properties = Property.objects.filter(is_active=True).select_related('developer', 'property_type', 'location')
    
    # Фильтры
    developer_slug = request.GET.get('developer')
    property_type = request.GET.get('type')
    location = request.GET.get('location')
    
    if developer_slug:
        properties = properties.filter(developer__slug=developer_slug)
    if property_type:
        properties = properties.filter(property_type__slug=property_type)
    if location:
        properties = properties.filter(location__slug=location)
    
    paginator = Paginator(properties, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'properties/property_list.html', {
        'properties': page_obj,
        'page_obj': page_obj,
        'types': PropertyType.objects.all(),
        'locations': Location.objects.all(),
    })


def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug, is_active=True)
    similar = Property.objects.filter(
        location=property.location, is_active=True
    ).exclude(pk=property.pk)[:4]
    
    return render(request, 'properties/property_detail.html', {
        'property': property,
        'similar_properties': similar,
    })