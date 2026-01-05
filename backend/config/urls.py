# config/urls.py
import os

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.i18n import set_language
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from core.sitemaps import StaticSitemap, BlogSitemap

sitemaps = {
    'static': StaticSitemap,
    'blog': BlogSitemap,
}

# --- URLs без языкового префикса ---
urlpatterns = [
    path("set-language/", set_language, name="set_language"),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("filer/", include("filer.urls")),
    path("blog/", include("blog.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
]

# --- Языковые маршруты ---
urlpatterns += i18n_patterns(
    # Allauth (authentication)
    path("account/", include("allauth.urls")),
    
    # Accounts (profile, subscriptions, etc.)
    path("account/", include("accounts.urls")),
    
    # Subscriptions & Checkout
    path("subscriptions/", include("subscriptions.urls")),
    
    # Deliveries & Tracking
    path("deliveries/", include("deliveries.urls")),
    
    # Core pages
    path("", include("core.urls")),
    
    prefix_default_language=False,
)

# === STATIC & MEDIA FILES ===
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Django Browser Reload
    if "django_browser_reload" in settings.INSTALLED_APPS:
        urlpatterns += [
            path("__reload__/", include("django_browser_reload.urls")),
        ]
    
    # Debug Toolbar
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns