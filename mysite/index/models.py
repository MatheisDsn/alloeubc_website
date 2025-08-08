from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import os

def validate_image_or_svg(value):
    """Validator pour accepter les images classiques et les fichiers SVG"""
    if value:
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
        if ext not in valid_extensions:
            raise ValidationError(f'Format de fichier non supporté. Formats acceptés : {", ".join(valid_extensions)}')
        
        # Pour les SVG, on skip la validation d'image
        if ext == '.svg':
            return value
            
        # Pour les autres formats, on vérifie que c'est bien une image
        try:
            get_image_dimensions(value)
        except Exception:
            raise ValidationError('Le fichier uploadé n\'est pas une image valide.')
    
    return value

class CustomImageField(models.FileField):
    """Champ personnalisé qui accepte les images et les SVG"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', []).append(validate_image_or_svg)
        super().__init__(*args, **kwargs)

class CarrousselImages(models.Model):
    image = models.ImageField(blank=False, upload_to='accueil/caroussel/')
    
    # Ordre d'affichage
    ordre = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage (0 = premier)")
    
    # Texte superposé optionnel
    titre = models.CharField(max_length=100, blank=True, help_text="Titre affiché sur l'image")
    sous_titre = models.CharField(max_length=200, blank=True, help_text="Sous-titre affiché sur l'image")
    description = models.TextField(max_length=300, blank=True, help_text="Description affichée sur l'image")
    
    # Bouton d'action optionnel
    texte_bouton = models.CharField(max_length=50, blank=True, help_text="Texte du bouton (ex: 'En savoir plus')")
    lien_bouton = models.URLField(blank=True, help_text="URL externe vers laquelle le bouton redirige")
    lien_interne = models.CharField(max_length=100, blank=True, help_text="Nom de l'URL Django (ex: 'index:equipes')")
    
    # Options d'affichage
    POSITION_CHOICES = [
        ('center', 'Centre'),
        ('left', 'Gauche'),
        ('right', 'Droite'),
        ('bottom-left', 'Bas gauche'),
        ('bottom-right', 'Bas droite'),
        ('top-left', 'Haut gauche'),
        ('top-right', 'Haut droite'),
    ]
    
    COULEUR_CHOICES = [
        ('white', 'Blanc'),
        ('black', 'Noir'),
        ('primary', 'Couleur primaire'),
    ]
    
    position_texte = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='center',
        help_text="Position du texte sur l'image"
    )
    
    couleur_texte = models.CharField(
        max_length=20,
        choices=COULEUR_CHOICES,
        default='white',
        help_text="Couleur du texte"
    )
    
    opacite_overlay = models.FloatField(
        default=0.4,
        help_text="Opacité du fond sombre (0.0 = transparent, 1.0 = opaque)"
    )
    vitesse_slider = models.PositiveIntegerField("Vitesse du slider (ms)", default=800, help_text="Durée de transition entre les slides en millisecondes")

    class Meta:
        verbose_name = "Défilement images"
        verbose_name_plural = "Défilement images"
        ordering = ['ordre']

    def __str__(self):
        if self.titre:
            return f"{self.ordre} - {self.titre}"
        return f"{self.ordre} - {os.path.basename(self.image.name)}"

class FAQ(models.Model):
    question = models.CharField(max_length=150)
    reponse = models.TextField(max_length=1000)
    ordre = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage (0 = premier)")

    class Meta:
        verbose_name = "Partie FAQ"
        verbose_name_plural = "Partie FAQ"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.ordre} - {self.question}"
    
class Organisation_card(models.Model):
    image_profile = models.ImageField(blank=True, upload_to='presentation/organisation/', null=True )
    nom = models.CharField(max_length=150)
    fonction = models.CharField(max_length=250)
    ordre = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage (0 = premier)")

    class Meta:
        verbose_name = "Organigramme bureau"
        verbose_name_plural = "Organigramme bureau"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.ordre} - {self.nom} - {self.fonction}"
    
class Entrainement(models.Model):
    image_entrainement = models.ImageField(blank=False, upload_to='informations/entraînements/' )

    class Meta:
        verbose_name = "Planning entraînement"
        verbose_name_plural = "Planning entraînement"

    def __str__(self):
        return os.path.basename(self.image_entrainement.name)

class PartenairesSponsor(models.Model):
    image_blanc = CustomImageField(
        blank=True, 
        upload_to='informations/part-spons/blanc/',
        help_text="Logo blanc/transparent - pour footer et barre défilante (Formats acceptés : JPG, PNG, GIF, BMP, WebP, SVG)"
    )
    image_noir = CustomImageField(
        blank=True, 
        upload_to='informations/part-spons/noir/',
        help_text="Logo noir/coloré - pour page informations (Formats acceptés : JPG, PNG, GIF, BMP, WebP, SVG)"
    )
    nom = models.CharField(max_length=150)
    fonction = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Partenaires et sponsors"
        verbose_name_plural = "Partenaires et sponsors"

    def __str__(self):
        return self.nom + ' ' + '/' + ' ' + self.fonction
    
class DocumentsFonctionnement(models.Model):
    nom = models.CharField(max_length=150)
    fichier = models.FileField(upload_to="informations/fonctionnement/")
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom + ' ' + '/' + ' ' + self.fichier.name
    
    class Meta:
        verbose_name = "Documents de fonctionnement"
        verbose_name_plural = "Documents de fonctionnement"
    
class Equipes(models.Model):
    nom = models.CharField(max_length=100)
    coach = models.CharField(max_length=100)
    coach_adjoint = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    class Meta:
        verbose_name = "Équipes"
        verbose_name_plural = "Équipes"

    def __str__(self):
        return self.nom + ' ' + '/' + ' ' + self.coach
    
class DocumentsDossierInscription(models.Model):
    nom = models.CharField(max_length=100)
    document = models.FileField(upload_to="inscriptions/documents-dossier-inscr/")

    class Meta:
        verbose_name = "Documents inscription"
        verbose_name_plural = "Documents inscription"

    def __str__(self):
        return self.nom + ' ' + '/' + ' ' + os.path.basename(self.document.name)