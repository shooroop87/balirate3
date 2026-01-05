from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    """Sitemap для статических страниц"""
    
    protocol = "https"
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            ("index", 1.0, "weekly"),
        ]

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class BlogSitemap(Sitemap):
    """Sitemap для блога"""
    
    protocol = "https"
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        from blog.models import BlogPost
        return BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()