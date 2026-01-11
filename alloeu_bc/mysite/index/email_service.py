"""
Service d'envoi d'emails via l'API Brevo pour les inscriptions à la soirée festive
"""
import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class BrevoEmailService:
    """Service pour envoyer des emails via Brevo API"""
    
    BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
    ADMIN_EMAILS = [
        "secretariat.alloeubc@gmail.com",
        "matheis.dsn.pro@gmail.com"
    ]
    HELLOASSO_URL = "https://www.helloasso.com/associations/alloeu-basket-club/evenements/soiree-festive-du-club"
    
    @classmethod
    def send_email(cls, to_email, to_name, subject, html_content):
        """
        Envoie un email via l'API Brevo
        
        Args:
            to_email: Email du destinataire
            to_name: Nom du destinataire
            subject: Sujet de l'email
            html_content: Contenu HTML de l'email
        
        Returns:
            True si l'email a été envoyé avec succès, False sinon
        """
        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json"
        }
        
        data = {
            "sender": {
                "name": settings.DEFAULT_FROM_NAME,
                "email": settings.DEFAULT_FROM_EMAIL
            },
            "to": [
                {
                    "email": to_email,
                    "name": to_name
                }
            ],
            "subject": subject,
            "htmlContent": html_content
        }
        
        try:
            response = requests.post(cls.BREVO_API_URL, json=data, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'envoi de l'email: {e}")
            return False
    
    @classmethod
    def send_confirmation_email(cls, inscription):
        """
        Envoie un email de confirmation à la personne inscrite
        
        Args:
            inscription: Instance de InscriptionSoiree
        """
        context = {
            'inscription': inscription,
            'participants': inscription.participants.all()
        }
        
        html_content = render_to_string('index/emails/soiree_confirmation.html', context)
        subject = "Confirmation de votre inscription à la soirée festive"
        
        return cls.send_email(
            to_email=inscription.email,
            to_name=f"{inscription.prenom} {inscription.nom}",
            subject=subject,
            html_content=html_content
        )
    
    @classmethod
    def send_admin_notification(cls, inscription, validation_url):
        """
        Envoie un email aux admins pour notifier d'une nouvelle inscription
        
        Args:
            inscription: Instance de InscriptionSoiree
            validation_url: URL complète pour valider l'inscription
        """
        context = {
            'inscription': inscription,
            'participants': inscription.participants.all(),
            'validation_url': validation_url
        }
        
        html_content = render_to_string('index/emails/soiree_admin_notification.html', context)
        subject = f"Nouvelle inscription soirée - {inscription.prenom} {inscription.nom}"
        
        # Envoyer à tous les admins
        success = True
        for admin_email in cls.ADMIN_EMAILS:
            result = cls.send_email(
                to_email=admin_email,
                to_name="Admin Alloeu BC",
                subject=subject,
                html_content=html_content
            )
            success = success and result
        
        return success
    
    @classmethod
    def send_validation_email(cls, inscription):
        """
        Envoie un email de validation avec le lien HelloAsso
        
        Args:
            inscription: Instance de InscriptionSoiree
        """
        context = {
            'inscription': inscription,
            'helloasso_url': cls.HELLOASSO_URL
        }
        
        html_content = render_to_string('index/emails/soiree_validation.html', context)
        subject = "Votre inscription à la soirée festive est validée !"
        
        return cls.send_email(
            to_email=inscription.email,
            to_name=f"{inscription.prenom} {inscription.nom}",
            subject=subject,
            html_content=html_content
        )
