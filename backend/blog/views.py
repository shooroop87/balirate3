from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogPost, BlogCategory


def blog_list(request):
    posts = BlogPost.objects.filter(status='published').select_related('category')
    
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'blog/blog_list.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'categories': BlogCategory.objects.all(),
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    related = BlogPost.objects.filter(
        status='published', category=post.category
    ).exclude(pk=post.pk)[:3]
    
    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'related_posts': related,
    })