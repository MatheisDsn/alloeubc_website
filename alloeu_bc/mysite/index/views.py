from django.shortcuts import render
from django.urls import reverse, NoReverseMatch
from .models import CarrousselImages, FAQ, Organisation_card, Entrainement, PartenairesSponsor, DocumentsFonctionnement, Equipes, DocumentsDossierInscription
from .services import get_next_matches, get_last_results


def index(requests):
    # Récupération des données des matchs depuis l'API
    next_matches = get_next_matches(limit=7)
    last_results = get_last_results(limit=7)
    
    # Récupération des slides avec résolution des URLs internes
    slides = CarrousselImages.objects.all().order_by('ordre')
    
    # Résoudre les URLs internes pour chaque slide
    for slide in slides:
        if slide.lien_interne:
            try:
                slide.resolved_url = reverse(slide.lien_interne)
            except (NoReverseMatch, ValueError):
                slide.resolved_url = '#'
        else:
            slide.resolved_url = None
    
    # Récupération des sponsors pour la barre défilante
    # Note: sponsors maintenant disponible globalement via context_processors
    
    context = {
        "sliders": slides,
        "FAQ": FAQ.objects.all().order_by('ordre'),
        "next_matches": next_matches,
        "last_results": last_results
    }
    
    return render(requests, 'index/accueil.html', context)

def presentation(requests):
    return render(requests, 'index/presentation.html', {"cards_inf" : Organisation_card.objects.all().order_by('ordre')})

def information(requests):
    return render(requests, 'index/informations.html', {"img_entrainement" : Entrainement.objects.first(), "cards" : PartenairesSponsor.objects.all(), "fichiers" : DocumentsFonctionnement.objects.all()})

def lesequipes(requests):
    return render(requests, 'index/equipes.html', {"lesequipes" : Equipes.objects.all()})

def inscriptions(requests):
    return render(requests, 'index/inscriptions.html', {"docs" : DocumentsDossierInscription.objects.all()})

def matches(request):
    """Vue pour afficher tous les matchs avec pagination et filtres"""
    # Paramètres de pagination
    limit = int(request.GET.get('limit', 10))
    page = int(request.GET.get('page', 1))
    offset = (page - 1) * limit
    
    # Filtres
    match_type = request.GET.get('type', 'all')  # 'next', 'past', 'all'
    
    if match_type == 'next':
        matches_data = get_next_matches(limit=50)  # Récupère plus de matchs
        title = "Prochains Matchs"
    elif match_type == 'past':
        matches_data = get_last_results(limit=50)
        title = "Résultats Précédents"
    else:
        # Récupère les deux types
        next_matches = get_next_matches(limit=25)
        past_matches = get_last_results(limit=25)
        matches_data = next_matches + past_matches
        title = "Tous les Matchs"
    
    # Pagination simple côté Python
    total_matches = len(matches_data)
    paginated_matches = matches_data[offset:offset + limit]
    
    context = {
        'matches': paginated_matches,
        'title': title,
        'match_type': match_type,
        'page': page,
        'limit': limit,
        'total_matches': total_matches,
        'has_next': offset + limit < total_matches,
        'has_previous': page > 1,
        'next_page': page + 1 if offset + limit < total_matches else None,
        'previous_page': page - 1 if page > 1 else None,
    }
    
    return render(request, 'index/matches.html', context)