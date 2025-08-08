from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()



class Produits(models.Model):
    nom = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, blank=True)
    prix = models.FloatField(default=0.0)
    description_principal = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True, max_length=1000)
    image = models.ImageField(blank=False, upload_to='boutique/', null=True)

    class Meta:
        verbose_name = "Produits"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("boutique:detail", kwargs={"slug": self.slug})
    


class Cart(models.Model):
    product_cart = models.ManyToManyField(Produits, through='CartItem')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de : {self.user}"

    class Meta:
        verbose_name = "Paniers des utilisateurs"
        verbose_name_plural = "Paniers des utilisateurs"
    
class CartItem(models.Model):
    product = models.ForeignKey(Produits, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    def __str__(self):
        return 'Produit :'

class StatutCommande(models.TextChoices):
    EN_ATTENTE = 'en_attente', 'en attente'
    EN_PREPARATION = 'en_cours', 'en préparation'
    PRETE = 'prete', 'prête'
    RECUPEREE = 'recuperee', 'récuperée'
    ANNULEE = 'annulee', 'annulée'

def generate_order_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Commande(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    produits_commandes = models.ManyToManyField(Produits, through='ArticleCommande')
    infos = models.TextField(blank=True, null=True)
    total = models.FloatField(default=0.0)
    numero_commande = models.CharField(max_length=10, unique=True, default=generate_order_number)  # Shorter unique code
    statut = models.CharField(
        max_length=20,
        choices=StatutCommande.choices,
        default=StatutCommande.EN_ATTENTE,
    )

    class Meta:
        verbose_name = "Commandes"
        verbose_name_plural = "Commandes"

    def save(self, *args, **kwargs):
        """ Sauvegarder la commande, calculer le total, puis sauvegarder à nouveau """
        # Sauvegarder la commande si elle est nouvelle
        if not self.pk:
            super().save(*args, **kwargs)
        
        # Calculer le total après que la commande soit sauvegardée
        self.total = self.calculer_total()
        
        # Sauvegarder la commande avec le total mis à jour
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.numero_commande:  # S'assurer qu'il n'est pas dupliqué
            self.numero_commande = generate_order_number()
        while Commande.objects.filter(numero_commande=self.numero_commande).exists():
            self.numero_commande = generate_order_number()
        super().save(*args, **kwargs)


    def calculer_total(self):
        """Calculer automatiquement le total de la commande."""
        total = 0
        articles = self.articlecommande_set.all()  # Récupérer tous les articles de la commande
        for article in articles:
            total += article.prix_article * article.quantite  # Prix unitaire * quantité
        return total


# articles commandé 1 par 1 mais en plusieurs quantité
class ArticleCommande(models.Model):
    article = models.ForeignKey(Produits, on_delete=models.SET_NULL, null=True, blank=True)
    nom_article = models.CharField(max_length=150, blank=True)
    prix_article = models.FloatField(default=0.0)
    quantite = models.IntegerField(default=1)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Si un produit est lié à cet article, on copie ses infos
        if self.article:
            self.nom_article = self.article.nom
            self.prix_article = self.article.prix
        super().save(*args, **kwargs)



