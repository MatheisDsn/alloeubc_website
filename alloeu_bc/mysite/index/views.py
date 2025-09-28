from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse, NoReverseMatch
from django.contrib import messages
from .models import CarrousselImages, FAQ, Organisation_card, Entrainement, Tarifs, PartenairesSponsor, DocumentsFonctionnement, Equipes, DocumentsDossierInscription
from annonces.models import Annonce
from .services import get_next_matches, get_last_results
from .forms import InscriptionForm
import logging
from smtplib import SMTPException
from socket import timeout as socket_timeout


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
        "last_results": last_results,
        # 1 ligne d'annonces (max 3)
        "home_annonces": Annonce.objects.filter(is_published=True).order_by('-created_at')[:3],
    # Formulaire d'inscription sur la page d'accueil
    "home_inscription_form": InscriptionForm(),
    }
    
    return render(requests, 'index/accueil.html', context)

def presentation(requests):
    return render(requests, 'index/presentation.html', {"cards_inf" : Organisation_card.objects.all().order_by('ordre')})

def information(requests):
    return render(requests, 'index/informations.html', {
        "img_entrainement": Entrainement.objects.first(), 
        "img_tarifs": Tarifs.objects.first(),
        "cards": PartenairesSponsor.objects.all(), 
        "fichiers": DocumentsFonctionnement.objects.all()
    })

def lesequipes(requests):
    # Ensure teams are ordered by the 'ordre' field so admin edits are reflected on the site
    return render(requests, 'index/equipes.html', {"lesequipes": Equipes.objects.all().order_by('ordre')})

def inscriptions(requests):
    success = False
    if requests.method == 'POST':
        form = InscriptionForm(requests.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            sexe = form.cleaned_data['sexe']
            birth_date = form.cleaned_data['birth_date']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            licensed_before = form.cleaned_data.get('licensed_before') or False

            # Email de confirmation au sportif
            subject_user = "Confirmation d'inscription - Alloeu Basket Club"
            sexe_label = dict(form.fields['sexe'].choices).get(sexe, sexe)
            html_user = (
                f"<p>Bonjour {full_name},</p>"
                f"<p>Nous avons bien reçu votre demande d'inscription. IMPORTANT : ce formulaire ne signifie <strong>pas</strong> encore l'inscription au club.</p>"
                f"<p>Prochaines étapes :</p>"
                f"<ul>"
                f"<li>Vous recevrez sous peu (ou dans les prochains jours) un e-mail de la Fédération pour compléter la licence.</li>"
                f"<li>Surveillez vos spams / courriers indésirables : l'e-mail peut s'y retrouver.</li>"
                f"</ul>"
                f"<p>Récapitulatif de votre demande :</p>"
                f"<ul>"
                f"<li>Nom et prénom : {full_name}</li>"
                f"<li>Sexe : {sexe_label}</li>"
                f"<li>Date de naissance : {birth_date:%d/%m/%Y}</li>"
                f"<li>E-mail : {email}</li>"
                f"<li>Téléphone : {phone}</li>"
                f"<li>Déjà licencié(e) : {'Oui' if licensed_before else 'Non'}</li>"
                f"</ul>"
                f"<p>Sportivement,<br>L'équipe Alloeu Basket Club</p>"
            )
            # Tentative d'envoi des emails avec gestion d'erreur
            logger = logging.getLogger(__name__)
            email_errors = []
            
            # Email de confirmation au sportif
            try:
                logger.info(f"Tentative d'envoi email confirmation à {email}")
                send_mail(
                    subject_user,
                    # plain fallback
                    f"Bonjour {full_name},\n\nNous avons bien reçu votre demande d'inscription. Notre secrétariat vous recontactera prochainement.\n\nNom et prénom: {full_name}\nDate de naissance: {birth_date:%d/%m/%Y}\nE-mail: {email}\nTéléphone: {phone}\nDéjà licencié(e): {'Oui' if licensed_before else 'Non'}\n\nSportivement,\nAlloeu Basket Club",
                    getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@alloeubasket.fr'),
                    [email],
                    html_message=html_user,
                )
                logger.info(f"Email confirmation envoyé avec succès à {email}")
            except (SMTPException, socket_timeout, Exception) as e:
                logger.error(f"Erreur envoi email confirmation à {email}: {str(e)}")
                email_errors.append(f"Email de confirmation: {str(e)}")

            # Email de notification au secrétariat
            subject_admin = "Nouvelle demande d'inscription - Site Alloeu BC"
            body_admin = (
                "Une nouvelle demande d'inscription a été soumise depuis le site."\
                f"\nNom et prénom : {full_name}"\
                f"\nSexe : {sexe_label}"\
                f"\nDate de naissance : {birth_date:%d/%m/%Y}"\
                f"\nE-mail : {email}"\
                f"\nTéléphone : {phone}"\
                f"\nDéjà licencié(e) : {'Oui' if licensed_before else 'Non'}"
            )
            try:
                logger.info("Tentative d'envoi email notification secrétariat")
                send_mail(
                    subject_admin,
                    body_admin,
                    getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@alloeubasket.fr'),
                    ['secretariat.alloeubc@gmail.com'],
                )
                logger.info("Email secrétariat envoyé avec succès")
            except (SMTPException, socket_timeout, Exception) as e:
                logger.error(f"Erreur envoi email secrétariat: {str(e)}")
                email_errors.append(f"Email secrétariat: {str(e)}")
            
            # Afficher un message selon le résultat des emails
            if email_errors:
                messages.warning(requests, f"Votre demande a été enregistrée mais il y a eu des problèmes d'envoi d'email. Contactez-nous si vous ne recevez pas de confirmation.")
                logger.warning(f"Inscription {full_name} ({email}) avec erreurs email: {email_errors}")
            else:
                messages.success(requests, "Votre demande d'inscription a été envoyée avec succès ! Vous allez recevoir un email de confirmation.")

            return redirect('index:index')
        # Form invalide: on laisse afficher les erreurs
        return render(requests, 'index/accueil.html', {
            "home_inscription_form": form,
            # Ajouter contenus minimaux pour éviter erreurs template si attendu
            "sliders": CarrousselImages.objects.all().order_by('ordre'),
            "FAQ": FAQ.objects.all().order_by('ordre'),
            "home_annonces": Annonce.objects.filter(is_published=True).order_by('-created_at')[:3],
            "next_matches": get_next_matches(limit=7),
            "last_results": get_last_results(limit=7),
        })
    else:
        form = InscriptionForm()
    # GET request: ré-afficher la page d'accueil avec le formulaire
    return render(requests, 'index/accueil.html', {
        "home_inscription_form": form,
        "sliders": CarrousselImages.objects.all().order_by('ordre'),
        "FAQ": FAQ.objects.all().order_by('ordre'),
        "home_annonces": Annonce.objects.filter(is_published=True).order_by('-created_at')[:3],
        "next_matches": get_next_matches(limit=7),
        "last_results": get_last_results(limit=7),
    })

def partenaires(request):
    """Page dédiée listant tous les partenaires."""
    cards = PartenairesSponsor.objects.prefetch_related('links').all()
    return render(request, 'index/partenaires.html', { 'cards': cards })

def matches(request):
    """Vue pour afficher tous les matchs avec pagination et filtres"""
    # Paramètres de pagination
    limit = int(request.GET.get('limit', 10))
    page = int(request.GET.get('page', 1))
    offset = (page - 1) * limit
    
    # Filtres
    match_type = request.GET.get('type', 'all')  # 'next', 'past', 'all'
    team_id_filter = request.GET.get('team')  # id numérique d'équipe du club (team_id)
    
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
    
    # Construire la liste des équipes du club disponibles dans les données
    club_teams = {}
    for m in matches_data:
        tid = m.get('club_team_id')
        tname = m.get('club_team_name')
        if tid and tname:
            club_teams[tid] = tname
    # Liste triée pour le template
    club_teams_list = sorted(
        [{'id': tid, 'name': tname} for tid, tname in club_teams.items()],
        key=lambda x: x['name']
    )

    # Filtrer par équipe si demandé
    if team_id_filter:
        try:
            team_id_int = int(team_id_filter)
            matches_data = [m for m in matches_data if m.get('club_team_id') == team_id_int]
        except ValueError:
            pass
    
    # Pagination simple côté Python
    total_matches = len(matches_data)
    paginated_matches = matches_data[offset:offset + limit]
    
    context = {
        'matches': paginated_matches,
        'title': title,
        'match_type': match_type,
        'team_id_filter': team_id_filter,
        'page': page,
        'limit': limit,
        'total_matches': total_matches,
        'has_next': offset + limit < total_matches,
        'has_previous': page > 1,
        'next_page': page + 1 if offset + limit < total_matches else None,
        'previous_page': page - 1 if page > 1 else None,
        'club_teams': club_teams,
        'club_teams_list': club_teams_list,
    }
    
    return render(request, 'index/matches.html', context)

def mentions_legales(request):
    return render(request, 'index/mentions_legales.html')
