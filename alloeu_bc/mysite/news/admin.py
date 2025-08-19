from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'article_count', 'created_at']
    list_filter = ['color', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def article_count(self, obj):
        count = obj.article_set.filter(status='published').count()
        return f"{count} article{'s' if count != 1 else ''}"
    article_count.short_description = "Articles publiés"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'category', 
        'status_display', 
        'featured',
        'author', 
        'published_at',
        'view_count'
    ]
    list_filter = [
        'status', 
        'featured', 
        'category', 
        'created_at', 
        'published_at'
    ]
    search_fields = ['title', 'excerpt', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'reading_time_display']
    
    fieldsets = (
        ('Contenu Principal', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content')
        }),
        ('Image', {
            'fields': ('image', 'image_alt'),
            'classes': ('collapse',)
        }),
        ('Publication', {
            'fields': ('status', 'featured', 'author', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Informations', {
            'fields': ('reading_time_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def status_display(self, obj):
        colors = {
            'published': '#10b981',  # green
            'draft': '#f59e0b',      # yellow  
            'archived': '#6b7280'    # gray
        }
        color = colors.get(obj.status, '#6b7280')
        
        # Ajout d'un indicateur si l'article est programmé
        extra = ""
        if obj.status == 'published' and obj.published_at and obj.published_at > timezone.now():
            extra = " (programmé)"
            color = '#3b82f6'  # blue
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}{}</span>',
            color,
            obj.get_status_display(),
            extra
        )
    status_display.short_description = "Statut"
    
    def reading_time_display(self, obj):
        return f"{obj.reading_time} min de lecture"
    reading_time_display.short_description = "Temps de lecture"
    
    def view_count(self, obj):
        # Placeholder pour un futur système de comptage des vues
        return "N/A"
    view_count.short_description = "Vues"
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        # Mettre à jour les dates de publication pour les articles qui n'en ont pas
        for article in queryset.filter(published_at__isnull=True):
            article.published_at = timezone.now()
            article.save()
        
        self.message_user(
            request, 
            f"{updated} article{'s' if updated != 1 else ''} publié{'s' if updated != 1 else ''}."
        )
    make_published.short_description = "Publier les articles sélectionnés"
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(
            request,
            f"{updated} article{'s' if updated != 1 else ''} mis en brouillon."
        )
    make_draft.short_description = "Mettre en brouillon"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(
            request,
            f"{updated} article{'s' if updated != 1 else ''} mis à la une."
        )
    make_featured.short_description = "Mettre à la une"
