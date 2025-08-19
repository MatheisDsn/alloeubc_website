from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from news.models import Article


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # Noms des routes existantes avec namespaces
        return [
            "index:index",
            "index:presentations",
            "index:informations",
            "index:lesequipes",
            "index:partenaires",
            "index:matches",
            "news:article_list",
            "boutique:index",
        ]

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        # Articles publiés et visibles
        return Article.objects.filter(status='published', published_at__lte=timezone.now())

    def lastmod(self, obj: Article):
        return obj.updated_at or obj.published_at

    def location(self, obj: Article):
        return obj.get_absolute_url()
