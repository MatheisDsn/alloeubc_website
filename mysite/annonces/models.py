from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Annonce(models.Model):
    CATEGORY_CHOICES = [
        ("vetements", "Vêtements"),
        ("chaussures", "Chaussures"),
        ("equipements", "Équipements"),
        ("autre", "Autre"),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    image = models.ImageField(upload_to="annonces/%Y/%m/", blank=True, null=True)

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
