from django.shortcuts import render, get_object_or_404
from .models import NewsPost, NewsCategory


def news_list(request):
    posts = NewsPost.objects.filter(status='published').order_by('-published_at')
    categories = NewsCategory.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug, status='published')
    categories = NewsCategory.objects.all()
    recent_posts = NewsPost.objects.filter(status='published').exclude(id=post.id)[:5]
    related_posts = NewsPost.objects.filter(status='published', category=post.category).exclude(id=post.id)[:3] if post.category else []
    
    # Навигация - с проверкой на None
    prev_post = None
    next_post = None
    if post.published_at:
        prev_post = NewsPost.objects.filter(status='published', published_at__lt=post.published_at).order_by('-published_at').first()
        next_post = NewsPost.objects.filter(status='published', published_at__gt=post.published_at).order_by('published_at').first()
    
    context = {
        'post': post,
        'categories': categories,
        'recent_posts': recent_posts,
        'related_posts': related_posts,
        'prev_post': prev_post,
        'next_post': next_post,
    }
    return render(request, 'news/news_detail.html', context)