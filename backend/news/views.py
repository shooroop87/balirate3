# blog/views.py
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .models import BlogCategory, BlogPost


def blog_list(request):
    """Список всех постов блога."""
    posts = BlogPost.objects.filter(
        status=BlogPost.Status.PUBLISHED
    ).select_related("category").order_by("-published_at")
    
    # Фильтр по категории
    category_slug = request.GET.get("category")
    category = None
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug)
        posts = posts.filter(category=category)
    
    # Пагинация
    paginator = Paginator(posts, 9)  # 9 постов на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # Все категории для фильтра
    categories = BlogCategory.objects.all()
    
    return render(request, "blog/blog_list.html", {
        "page_obj": page_obj,
        "categories": categories,
        "current_category": category,
    })


def blog_detail(request, slug):
    """Детальная страница поста."""
    post = get_object_or_404(
        BlogPost.objects.select_related("category"),
        slug=slug,
        status=BlogPost.Status.PUBLISHED
    )
    
    # Похожие посты (из той же категории)
    related_posts = []
    if post.category:
        related_posts = BlogPost.objects.filter(
            category=post.category,
            status=BlogPost.Status.PUBLISHED
        ).exclude(id=post.id)[:3]
    
    return render(request, "blog/blog_detail.html", {
        "post": post,
        "related_posts": related_posts,
    })