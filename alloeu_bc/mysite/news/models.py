from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image


class Category(models.Model):
    """Catégories pour organiser les articles"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    color = models.CharField(
        max_length=20, 
        default='blue',
        choices=[
            ('blue', 'Bleu'),
            ('green', 'Vert'), 
            ('red', 'Rouge'),
            ('yellow', 'Jaune'),
            ('purple', 'Violet'),
            ('pink', 'Rose'),
            ('gray', 'Gris'),
        ],
        verbose_name="Couleur"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Articles de news/actualités"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Catégorie"
    )
    excerpt = models.TextField(
        max_length=300, 
        verbose_name="Résumé",
        help_text="Court résumé qui apparaîtra dans la liste des articles"
    )
    content = models.TextField(verbose_name="Contenu")
    image = models.ImageField(
        upload_to='news/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Image principale"
    )
    image_alt = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Texte alternatif de l'image",
        help_text="Description de l'image pour l'accessibilité"
    )
    
    # Métadonnées
    author = models.CharField(
        max_length=100,
        default="Alloeu Basket Club",
        verbose_name="Auteur"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Statut"
    )
    featured = models.BooleanField(
        default=False,
        verbose_name="Article à la une",
        help_text="L'article apparaîtra en premier dans la liste"
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Publié le",
        help_text="Laissez vide pour publication immédiate"
    )
    
    # SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Meta description",
        help_text="Description pour les moteurs de recherche (max 160 caractères)"
    )

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Génération automatique du slug
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Si l'article passe en statut publié et n'a pas de date de publication
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        # Génération automatique de la meta description si vide
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]

        super().save(*args, **kwargs)

        # Redimensionnement de l'image si nécessaire
        if self.image:
            self.resize_image()

    def resize_image(self):
        """Redimensionne l'image pour optimiser les performances"""
        try:
            with Image.open(self.image.path) as img:
                # Redimensionner si l'image est trop grande
                max_size = (1200, 800)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    img.save(self.image.path, optimize=True, quality=85)
        except Exception:
            pass  # Si erreur, on ignore le redimensionnement

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug})

    @property
    def is_published(self):
        """Vérifie si l'article est publié et visible"""
        if self.status != 'published':
            return False
        if self.published_at and self.published_at > timezone.now():
            return False
        return True

    @property
    def reading_time(self):
        """Estime le temps de lecture en minutes"""
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))  # ~200 mots par minute

    def get_related_articles(self, limit=3):
        """Retourne des articles similaires"""
        related = Article.objects.filter(
            status='published',
            category=self.category
        ).exclude(id=self.id)
        
        if self.published_at:
            related = related.filter(published_at__lte=timezone.now())
        
        return related[:limit]
