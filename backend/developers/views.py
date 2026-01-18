from django.shortcuts import render, get_object_or_404
from .models import Developer, DeveloperCategory


def developer_list(request):
    developers = Developer.objects.filter(is_active=True).select_related('category')
    categories = DeveloperCategory.objects.all()
    
    # Фильтр по категории
    category_slug = request.GET.get('category')
    if category_slug:
        developers = developers.filter(category__slug=category_slug)
    
    return render(request, 'developers/developer_list.html', {
        'developers': developers,
        'categories': categories,
        'current_category': category_slug,
    })


def developer_detail(request, slug):
    developer = get_object_or_404(Developer, slug=slug, is_active=True)
    properties = developer.properties.filter(is_active=True)[:6]
    reviews = developer.reviews.filter(is_approved=True)
    
    return render(request, 'developers/developer_detail.html', {
        'developer': developer,
        'properties': properties,
        'reviews': reviews,
    })