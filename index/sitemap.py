from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone


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
        ]

    def location(self, item):
        return reverse(item)

