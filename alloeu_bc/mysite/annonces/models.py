from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
import os
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField


def validate_image_or_svg(value):
    """Validator pour accepter les images classiques et les fichiers SVG (Cloudinary ou fichiers classiques)."""
    if not value:
        return value

    # Gestion spéciale pour CloudinaryResource
    if hasattr(value, "resource_type"):
        if value.resource_type == "image" or getattr(value, "format", None) == "svg":
            return value
        raise ValidationError("Le fichier Cloudinary doit être une image ou un SVG")

    # Gestion pour les fichiers normaux
    ext = os.path.splitext(getattr(value, "name", ""))[1].lower()
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"]
    if ext and ext not in valid_extensions:
        raise ValidationError(
            f"Format de fichier non supporté. Formats acceptés : {', '.join(valid_extensions)}"
        )
    return value


class CustomCloudinaryField(CloudinaryField):
    """Champ Cloudinary acceptant images et SVG (resource_type auto)."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("resource_type", "auto")
        super().__init__(*args, **kwargs)


class Annonce(models.Model):
    CATEGORY_CHOICES = [
        ("vetements", "Vêtements"),
        ("chaussures", "Chaussures"),
        ("equipements", "Équipements"),
        ("autre", "Autre"),
    ]

    ETAT_CHOICES = [
        ("neuf", "Neuf"),
        ("tres_bon", "Très bon état"),
        ("bon", "Bon état"),
        ("correct", "État correct"),
        ("use", "Usé"),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # État/condition de l'article
    etat = models.CharField(
        max_length=20,
        choices=ETAT_CHOICES,
        default="bon",
        help_text="Condition de l'article",
    )

    image = CustomCloudinaryField(
        "image",
        folder="annonces",
        blank=True,
        null=True,
        validators=[validate_image_or_svg],
    )
    image2 = CustomCloudinaryField(
        "image",
        folder="annonces",
        blank=True,
        null=True,
        validators=[validate_image_or_svg],
    )

    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)

    # Prix en euros
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Prix en euros (0 pour gratuit)",
    )

    # Publication workflow
    is_published = models.BooleanField(default=False)
    publish_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    delete_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({'publiée' if self.is_published else 'en attente'})"
