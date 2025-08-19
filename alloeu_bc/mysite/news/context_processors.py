from django.utils import timezone
from .models import Article


def latest_articles(request):
    """Context processor pour avoir accès aux derniers articles partout"""
    latest_news = Article.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).order_by('-featured', '-published_at')[:3]  # Seulement 3 articles
    
    return {
        'latest_news': latest_news,
    }
