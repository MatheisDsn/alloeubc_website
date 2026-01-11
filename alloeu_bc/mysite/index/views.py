from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import (CarrousselImages, FAQ, Organisation_card, Entrainement, Tarifs, 
                     PartenairesSponsor, DocumentsFonctionnement, Equipes, 
                     DocumentsDossierInscription, InscriptionSoiree, ParticipantSoiree)
from annonces.models import Annonce
from .services import get_next_matches, get_last_results
from .forms import InscriptionForm, InscriptionSoireeForm
from .email_service import BrevoEmailService
import logging
import requests as http_requests
from datetime import datetime


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
            participation_roles = form.cleaned_data.get('participation_roles') or []

            # Email de confirmation au sportif
            subject_user = "Confirmation d'inscription - Alloeu Basket Club"
            sexe_label = dict(form.fields['sexe'].choices).get(sexe, sexe)
            
            # Tentative d'envoi des emails avec Brevo
            logger = logging.getLogger(__name__)
            email_errors = []
            
            brevo_url = "https://api.brevo.com/v3/smtp/email"
            brevo_headers = {
                "accept": "application/json",
                "api-key": settings.BREVO_API_KEY,
                "content-type": "application/json"
            }
            
            # Préparer les données pour les templates
            current_datetime = datetime.now()
            
            # Debug: log pour vérifier le format de date
            logger.info(f"Date reçue du formulaire: {birth_date} (type: {type(birth_date)})")
            
            # Formatage sécurisé de la date
            if isinstance(birth_date, str):
                # Si c'est une chaîne, essayer de la parser
                try:
                    from datetime import datetime as dt
                    parsed_date = dt.strptime(birth_date, '%Y-%m-%d')
                    formatted_birth_date = parsed_date.strftime('%d/%m/%Y')
                except ValueError:
                    try:
                        parsed_date = dt.strptime(birth_date, '%d/%m/%Y')
                        formatted_birth_date = birth_date  # Déjà au bon format
                    except ValueError:
                        formatted_birth_date = str(birth_date)  # Fallback
            else:
                # Si c'est un objet date/datetime
                formatted_birth_date = birth_date.strftime('%d/%m/%Y')
            
            logger.info(f"Date formatée pour email: {formatted_birth_date}")
            
            # Libellés lisibles pour les rôles multiples
            roles_labels = []
            if participation_roles:
                choices_map = dict(form.fields['participation_roles'].choices)
                roles_labels = [choices_map.get(r, r) for r in participation_roles]

            email_context = {
                'full_name': full_name,
                'sexe_label': sexe_label,
                'birth_date': formatted_birth_date,
                'email': email,
                'phone': phone,
                'licensed_before_text': 'Oui' if licensed_before else 'Non',
                'participation_roles': roles_labels,
                'current_date': current_datetime.strftime('%d/%m/%Y'),
                'current_time': current_datetime.strftime('%H:%M'),
            }
            
            # Email de confirmation au sportif avec template HTML
            try:
                logger.info(f"Tentative d'envoi email confirmation à {email}")
                logger.info(f"FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
                logger.info(f"BREVO_API_KEY présente: {bool(settings.BREVO_API_KEY)}")
                
                # Générer le HTML depuis le template
                html_content = render_to_string('index/emails/inscription_confirmation.html', email_context)
                logger.info(f"Template rendu avec succès, longueur HTML: {len(html_content)}")
                
                payload_user = {
                    "sender": {
                        "name": settings.DEFAULT_FROM_NAME,
                        "email": settings.DEFAULT_FROM_EMAIL
                    },
                    "to": [{"email": email, "name": full_name}],
                    "subject": subject_user,
                    "htmlContent": html_content
                }
                
                response = http_requests.post(brevo_url, json=payload_user, headers=brevo_headers)
                
                if response.status_code == 201:
                    logger.info(f"Email confirmation envoyé à {email} - Status: {response.status_code}")
                    logger.info(f"Message ID: {response.json().get('messageId')}")
                else:
                    logger.error(f"Erreur Brevo: {response.status_code} - {response.text}")
                    email_errors.append(f"Email de confirmation: {response.text}")
            except Exception as e:
                import traceback
                logger.error(f"Erreur envoi email confirmation à {email}: {str(e)}")
                logger.error(f"Type d'erreur: {type(e).__name__}")
                logger.error(f"Traceback complet:\n{traceback.format_exc()}")
                email_errors.append(f"Email de confirmation: {str(e)}")

            # Email de notification au secrétariat avec template HTML
            subject_admin = "Nouvelle demande d'inscription - Site Alloeu BC"
            try:
                logger.info("Tentative d'envoi email notification secrétariat")
                
                # Générer le HTML depuis le template
                html_admin = render_to_string('index/emails/inscription_admin.html', email_context)
                logger.info(f"Template admin rendu, longueur HTML: {len(html_admin)}")
                
                payload_admin = {
                    "sender": {
                        "name": settings.DEFAULT_FROM_NAME,
                        "email": settings.DEFAULT_FROM_EMAIL
                    },
                    "to": [
                        {"email": "secretariat.alloeubc@gmail.com", "name": "Secrétariat Alloeu BC"},
                        {"email": "site.alloeubc@gmail.com", "name": "Site Alloeu BC"}
                    ],
                    "subject": subject_admin,
                    "htmlContent": html_admin
                }
                
                response = http_requests.post(brevo_url, json=payload_admin, headers=brevo_headers)
                
                if response.status_code == 201:
                    logger.info(f"Email secrétariat envoyé - Status: {response.status_code}")
                    logger.info(f"Message ID: {response.json().get('messageId')}")
                else:
                    logger.error(f"Erreur Brevo admin: {response.status_code} - {response.text}")
                    email_errors.append(f"Email secrétariat: {response.text}")
            except Exception as e:
                import traceback
                logger.error(f"Erreur envoi email secrétariat: {str(e)}")
                logger.error(f"Type d'erreur: {type(e).__name__}")
                logger.error(f"Traceback complet:\n{traceback.format_exc()}")
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


def inscription_soiree(request):
    """Vue pour le formulaire d'inscription à la soirée festive"""
    if request.method == 'POST':
        form = InscriptionSoireeForm(request.POST)
        
        if form.is_valid():
            # Créer l'inscription
            inscription = InscriptionSoiree.objects.create(
                nom=form.cleaned_data['nom'],
                prenom=form.cleaned_data['prenom'],
                email=form.cleaned_data['email'],
                telephone=form.cleaned_data['telephone'],
                nombre_personnes=form.cleaned_data['nombre_personnes']
            )
            
            # Créer les participants
            for i in range(1, form.cleaned_data['nombre_personnes'] + 1):
                lien_club = form.cleaned_data.get(f'lien_club_{i}', '')
                if lien_club:
                    ParticipantSoiree.objects.create(
                        inscription=inscription,
                        lien_club=lien_club
                    )
            
            # Envoyer l'email de confirmation à l'inscrit
            BrevoEmailService.send_confirmation_email(inscription)
            
            # Construire l'URL complète pour le panel admin Django
            admin_url = reverse('index:admin_soiree')
            validation_url = request.build_absolute_uri('/admin/login/?next=' + admin_url)
            
            # Envoyer la notification aux admins
            BrevoEmailService.send_admin_notification(inscription, validation_url)
            
            messages.success(
                request,
                "Votre inscription a bien été enregistrée ! Vous allez recevoir un email de confirmation."
            )
            return redirect('index:inscription_soiree_success')
        else:
            messages.error(
                request,
                "Une erreur s'est produite. Veuillez vérifier les informations saisies."
            )
    else:
        # Récupérer le nombre de personnes depuis GET si présent
        nombre_personnes = request.GET.get('nombre_personnes')
        initial_data = {}
        if nombre_personnes:
            try:
                initial_data['nombre_personnes'] = int(nombre_personnes)
            except (ValueError, TypeError):
                pass
        
        form = InscriptionSoireeForm(initial=initial_data)
    
    context = {
        'form': form,
    }
    return render(request, 'index/inscription_soiree.html', context)


def inscription_soiree_success(request):
    """Page de confirmation après inscription"""
    return render(request, 'index/inscription_soiree_success.html')


@login_required
def admin_soiree(request):
    """Panel admin pour gérer les inscriptions"""
    inscriptions = InscriptionSoiree.objects.all().prefetch_related('participants')
    
    # Calculer les statistiques
    total_inscriptions = inscriptions.count()
    inscriptions_en_attente = inscriptions.filter(statut='en_attente').count()
    inscriptions_validees = inscriptions.filter(statut='valide').count()
    
    context = {
        'inscriptions': inscriptions,
        'total_inscriptions': total_inscriptions,
        'inscriptions_en_attente': inscriptions_en_attente,
        'inscriptions_validees': inscriptions_validees,
    }
    return render(request, 'index/admin_soiree.html', context)


@login_required
def valider_inscription(request, inscription_id):
    """Valider une inscription et envoyer l'email avec le lien HelloAsso"""
    inscription = get_object_or_404(InscriptionSoiree, id=inscription_id)
    
    if inscription.statut != 'valide':
        inscription.statut = 'valide'
        inscription.date_validation = timezone.now()
        inscription.save()
        
        # Envoyer l'email de validation avec le lien HelloAsso
        BrevoEmailService.send_validation_email(inscription)
        
        messages.success(
            request,
            f"L'inscription de {inscription.prenom} {inscription.nom} a été validée et un email lui a été envoyé."
        )
    else:
        messages.info(
            request,
            f"L'inscription de {inscription.prenom} {inscription.nom} était déjà validée."
        )
    
    return redirect('index:admin_soiree')


@login_required
def refuser_inscription(request, inscription_id):
    """Refuser une inscription"""
    inscription = get_object_or_404(InscriptionSoiree, id=inscription_id)
    
    inscription.statut = 'refuse'
    inscription.save()
    
    messages.warning(
        request,
        f"L'inscription de {inscription.prenom} {inscription.nom} a été refusée."
    )
    
    return redirect('index:admin_soiree')
