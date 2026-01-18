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
    """Детальная страница поста."""
    post = get_object_or_404(
        BlogPost.objects.select_related("category"),
        slug=slug,
        status=BlogPost.Status.PUBLISHED
    )
    
    # Категории для сайдбара
    categories = BlogCategory.objects.all()
    
    # Последние посты для сайдбара (кроме текущего)
    recent_posts = BlogPost.objects.filter(
        status=BlogPost.Status.PUBLISHED
    ).exclude(id=post.id).order_by("-published_at")[:5]
    
    # Похожие посты (из той же категории)
    related_posts = []
    if post.category:
        related_posts = BlogPost.objects.filter(
            category=post.category,
            status=BlogPost.Status.PUBLISHED
        ).exclude(id=post.id)[:3]
    
    # Навигация (предыдущий/следующий)
    prev_post = BlogPost.objects.filter(
        status=BlogPost.Status.PUBLISHED,
        published_at__lt=post.published_at
    ).order_by("-published_at").first()
    
    next_post = BlogPost.objects.filter(
        status=BlogPost.Status.PUBLISHED,
        published_at__gt=post.published_at
    ).order_by("published_at").first()
    
    return render(request, "blog/blog_detail.html", {
        "post": post,
        "categories": categories,
        "recent_posts": recent_posts,
        "related_posts": related_posts,
        "prev_post": prev_post,
        "next_post": next_post,
    })