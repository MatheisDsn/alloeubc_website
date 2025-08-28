from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import os
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import RawMediaCloudinaryStorage

def validate_image_or_svg(value):
    """Validator pour accepter les images classiques et les fichiers SVG"""
    if not value:
        return value
        
    # Gestion spéciale pour CloudinaryResource
    if hasattr(value, 'resource_type'):
        # C'est une ressource Cloudinary
        if value.resource_type == 'image' or value.format == 'svg':
            return value
        raise ValidationError('Le fichier Cloudinary doit être une image ou un SVG')
    
    # Gestion pour les fichiers normaux
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
    
    if ext not in valid_extensions:
        raise ValidationError(f'Format de fichier non supporté. Formats acceptés : {", ".join(valid_extensions)}')
    
    if ext == '.svg':
        return value
        
    try:
        get_image_dimensions(value)
    except Exception:
        raise ValidationError('Le fichier uploadé n\'est pas une image valide.')
    return value

class CustomCloudinaryField(CloudinaryField):
    """Champ personnalisé Cloudinary qui accepte les images et les SVG"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('resource_type', 'auto')
        super().__init__(*args, **kwargs)

class CarrousselImages(models.Model):
    image = CustomCloudinaryField(
        'image',
        folder='accueil/caroussel',
        blank=False,
        validators=[validate_image_or_svg]
    )
    ordre = models.PositiveIntegerField(default=0)
    titre = models.CharField(max_length=100, blank=True)
    sous_titre = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=300, blank=True)
    texte_bouton = models.CharField(max_length=50, blank=True)
    lien_bouton = models.URLField(blank=True)
    lien_interne = models.CharField(max_length=100, blank=True)
    
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
    
    position_texte = models.CharField(max_length=20, choices=POSITION_CHOICES, default='center')
    couleur_texte = models.CharField(max_length=20, choices=COULEUR_CHOICES, default='white')
    opacite_overlay = models.FloatField(default=0.4)
    vitesse_slider = models.PositiveIntegerField(default=800)

    class Meta:
        verbose_name = "Défilement images"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.ordre} - {self.titre}" if self.titre else f"{self.ordre} - {self.image.public_id}"

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
    image_profile = CustomCloudinaryField(
        'image',
        folder='presentation/organisation',
        blank=True,
        null=True,
        validators=[validate_image_or_svg]
    )
    nom = models.CharField(max_length=150)
    fonction = models.CharField(max_length=250)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Organigramme bureau"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.ordre} - {self.nom}"
    
class Entrainement(models.Model):
    image_entrainement = CustomCloudinaryField(
        'image',
        folder='informations/entrainements',
        blank=False
    )

    class Meta:
        verbose_name = "Planning entraînement"
        verbose_name_plural = "Planning entraînement"

    def __str__(self):
        return self.image_entrainement.public_id.split('/')[-1]  # Meilleure représentation

class Tarifs(models.Model):
    image_tarifs = CustomCloudinaryField(
        'image',
        folder='informations/tarifs',
        blank=False
    )

    class Meta:
        verbose_name = "Tarifs"
        verbose_name_plural = "Tarifs"

    def __str__(self):
        return self.image_tarifs.public_id.split('/')[-1]

class PartenairesSponsor(models.Model):
    image_blanc = CustomCloudinaryField(
        'image',
        folder='informations/part-spons/blanc',
        blank=True,
        validators=[validate_image_or_svg]
    )
    image_noir = CustomCloudinaryField(
        'image',
        folder='informations/part-spons/noir',
        blank=True,
        validators=[validate_image_or_svg]
    )
    nom = models.CharField(max_length=150)
    fonction = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Partenaires et sponsors"

    def __str__(self):
        return f"{self.nom} / {self.fonction}"

class SponsorLink(models.Model):
    sponsor = models.ForeignKey(PartenairesSponsor, related_name='links', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.URLField()

    class Meta:
        verbose_name = "Lien du sponsor"
        verbose_name_plural = "Liens du sponsor"
        ordering = ['id']

    def __str__(self):
        return f"{self.sponsor.nom} - {self.title}"
    
class DocumentsFonctionnement(models.Model):
    nom = models.CharField(max_length=150)
    fichier = models.FileField(
        storage=RawMediaCloudinaryStorage(),
        upload_to='informations/fonctionnement/'
    )
    date_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Documents de fonctionnement"
        verbose_name_plural = "Documents de fonctionnement"

    def __str__(self):
        return f"{self.nom} / {os.path.basename(self.fichier.name)}"
    
class Equipes(models.Model):
    nom = models.CharField(max_length=100)
    coach = models.CharField(max_length=100)
    coach_adjoint = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    ordre = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage (0 = premier)")

    class Meta:
        verbose_name = "Équipes"
        verbose_name_plural = "Équipes"
    ordering = ['ordre']

    def __str__(self):
        return self.nom + ' ' + '/' + ' ' + self.coach
    
class DocumentsDossierInscription(models.Model):
    nom = models.CharField(max_length=100)
    document = models.FileField(
        storage=RawMediaCloudinaryStorage(),
        upload_to='inscriptions/documents-dossier-inscr/'
    )

    class Meta:
        verbose_name = "Documents inscription"
        verbose_name_plural = "Documents inscription"

    def __str__(self):
        return f"{self.nom} / {os.path.basename(self.document.name)}"
