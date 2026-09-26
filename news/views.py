from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from .models import Article, Category


def article_list(request):
    """Liste des articles avec pagination et filtres"""
    articles = Article.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).select_related('category')
    
    # Filtrage par catégorie
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    
    # Recherche
    search_query = request.GET.get('search')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Articles à la une en premier
    articles = articles.order_by('-featured', '-published_at')
    
    # Pagination
    paginator = Paginator(articles, 9)  # 9 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Catégories pour le menu de filtrage
    categories = Category.objects.all()
    
    # Article à la une pour la hero section
    featured_article = articles.filter(featured=True).first()
    
    context = {
        'page_obj': page_obj,
        'articles': page_obj.object_list,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'featured_article': featured_article,
    }
    
    return render(request, 'news/article_list.html', context)


def article_detail(request, slug):
    """Détail d'un article"""
    article = get_object_or_404(
        Article.objects.select_related('category'),
        slug=slug,
        status='published',
        published_at__lte=timezone.now()
    )
    
    # Articles similaires
    related_articles = article.get_related_articles()
    
    # Articles récents (excluant l'article actuel)
    recent_articles = Article.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).exclude(id=article.id)[:5]
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'recent_articles': recent_articles,
    }
    
    return render(request, 'news/article_detail.html', context)