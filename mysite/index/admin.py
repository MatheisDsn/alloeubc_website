from django.contrib import admin
from django.utils.html import mark_safe
from django.urls import reverse
from adminsortable2.admin import SortableAdminMixin
from index.models import *

@admin.register(CarrousselImages)
class CarrousselImagesAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['ordre', 'image_preview', 'titre', 'sous_titre', 'has_button', 'position_texte']
    list_editable = ['titre', 'sous_titre']
    
    fieldsets = (
        ('Image', {
            'fields': ('image',)
        }),
        ('Contenu textuel', {
            'fields': ('titre', 'sous_titre', 'description'),
            'classes': ('collapse',),
        }),
        ('Bouton d\'action', {
            'fields': ('texte_bouton', 'lien_bouton', 'lien_interne'),
            'classes': ('collapse',),
            'description': 'Configurez un bouton optionnel (utilisez soit le lien externe, soit le lien interne)'
        }),
        ('Apparence', {
            'fields': ('position_texte', 'couleur_texte', 'opacite_overlay'),
            'classes': ('collapse',),
        }),
        ('Options', {
            'fields': ('vitesse_slider',),
            'classes': ('collapse',),
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 60px; max-width: 100px; object-fit: cover; border-radius: 4px;"/>')
        return "Pas d'image"
    image_preview.short_description = "Aperçu"
    
    def has_button(self, obj):
        return bool(obj.texte_bouton and (obj.lien_bouton or obj.lien_interne))
    has_button.short_description = "Bouton"
    has_button.boolean = True
    
    class Media:
        css = {
            'all': ('admin/css/carrousel_admin.css',)
        }
        js = ('admin/js/carrousel_admin.js',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'ordre', 'reponse_preview']
    list_editable = ['ordre']
    list_display_links = ['question']
    search_fields = ['question', 'reponse']
    ordering = ['ordre']
    
    def reponse_preview(self, obj):
        if len(obj.reponse) > 100:
            return obj.reponse[:100] + "..."
        return obj.reponse
    reponse_preview.short_description = "Réponse (aperçu)"
    
    fieldsets = (
        ('Ordre d\'affichage', {
            'fields': ('ordre',),
            'description': 'Définissez l\'ordre d\'affichage (0 = premier, 1 = deuxième, etc.)'
        }),
        ('Contenu', {
            'fields': ('question', 'reponse'),
        }),
    )

@admin.register(Organisation_card)
class OrganisationCardAdmin(admin.ModelAdmin):
    list_display = ['nom', 'fonction', 'ordre', 'image_preview']
    list_editable = ['ordre']
    list_display_links = ['nom']
    search_fields = ['nom', 'fonction']
    ordering = ['ordre']
    
    def image_preview(self, obj):
        if obj.image_profile:
            return mark_safe(f'<img src="{obj.image_profile.url}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 50%;"/>')
        return "Pas d'image"
    image_preview.short_description = "Photo"
    
    fieldsets = (
        ('Ordre d\'affichage', {
            'fields': ('ordre',),
            'description': 'Définissez l\'ordre d\'affichage (0 = premier, 1 = deuxième, etc.)'
        }),
        ('Informations personnelles', {
            'fields': ('nom', 'fonction'),
        }),
        ('Photo', {
            'fields': ('image_profile',),
        }),
    )

admin.site.register(Entrainement)
admin.site.register(PartenairesSponsor)