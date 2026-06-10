from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from index.sitemap import StaticViewSitemap, NewsSitemap
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("index.urls", namespace='index')),
    path("actualites/", include("news.urls", namespace='news')),
    path("log/", include("accounts.urls", namespace='accounts')),
        path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": {"static": StaticViewSitemap, "news": NewsSitemap}}, name="sitemap"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)