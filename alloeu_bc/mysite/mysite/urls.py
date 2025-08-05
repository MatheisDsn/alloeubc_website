from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("index.urls", namespace='index')),
    path("boutique/", include("boutique.urls", namespace='boutique')),
    path("actualites/", include("news.urls", namespace='news')),
    path("log/", include("accounts.urls", namespace='accounts')),
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)