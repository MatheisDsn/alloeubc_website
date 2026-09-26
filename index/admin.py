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
admin.site.register(Tarifs)

@admin.register(PartenairesSponsor)
class PartenairesSponsorAdmin(admin.ModelAdmin):
    list_display = ['nom', 'fonction', 'has_image_blanc', 'has_image_noir', 'image_blanc_preview', 'image_noir_preview']
    list_display_links = ['nom']
    search_fields = ['nom', 'fonction']
    inlines = []

    def has_image_blanc(self, obj):
        return bool(obj.image_blanc)
    has_image_blanc.boolean = True
    has_image_blanc.short_description = "Image blanc"

    def has_image_noir(self, obj):
        return bool(obj.image_noir)
    has_image_noir.boolean = True
    has_image_noir.short_description = "Image noir"

    def image_blanc_preview(self, obj):
        if obj.image_blanc:
            return mark_safe(f'<img src="{obj.image_blanc.url}" style="max-height:40px; max-width:80px; object-fit:contain; border-radius:4px;"/>')
        return "-"
    image_blanc_preview.short_description = "Aperçu blanc"

    def image_noir_preview(self, obj):
        if obj.image_noir:
            return mark_safe(f'<img src="{obj.image_noir.url}" style="max-height:40px; max-width:80px; object-fit:contain; border-radius:4px;"/>')
        return "-"
    image_noir_preview.short_description = "Aperçu noir"

class SponsorLinkInline(admin.TabularInline):
    model = SponsorLink
    extra = 1
    fields = ('title', 'url')

PartenairesSponsorAdmin.inlines = [SponsorLinkInline]

@admin.register(Equipes)
class EquipesAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['ordre', 'nom', 'coach', 'coach_adjoint', 'photo_preview', 'short_description']
    list_editable = ['ordre']
    list_display_links = ['nom']
    search_fields = ['nom', 'coach', 'coach_adjoint', 'description']
    list_filter = ['coach']
    ordering = ['ordre']
    sortable_field_name = 'ordre'

    actions = ['rebuild_order']

    def rebuild_order(self, request, queryset):
        """Rebuild ordre for all Equipes to be contiguous starting from 0.

        Useful if the drag & drop produced inconsistent or duplicate ordre values.
        """
        # Use the full queryset in admin ordering to ensure consistent assignment
        qs = self.get_queryset(request).order_by('ordre', 'id')
        for idx, obj in enumerate(qs):
            if obj.ordre != idx:
                obj.ordre = idx
                obj.save()
        self.message_user(request, "Ordre réinitialisé pour toutes les équipes.")
    rebuild_order.short_description = "Réinitialiser l'ordre des équipes"

    def short_description(self, obj):
        if not obj.description:
            return '-'
        return (obj.description[:60] + '...') if len(obj.description) > 60 else obj.description
    short_description.short_description = 'Description'

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' style='height:50px;width:50px;object-fit:cover;border-radius:6px;' />")
        return '-'
    photo_preview.short_description = 'Photo'


# Admin pour les inscriptions à la soirée festive
class ParticipantSoireeInline(admin.TabularInline):
    model = ParticipantSoiree
    extra = 0
    fields = ['lien_club']
    verbose_name = "Participant"
    verbose_name_plural = "Participants"


@admin.register(InscriptionSoiree)
class InscriptionSoireeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'prenom', 'email', 'telephone', 'nombre_personnes', 'statut_badge', 'date_inscription']
    list_filter = ['statut', 'date_inscription']
    search_fields = ['nom', 'prenom', 'email', 'telephone']
    readonly_fields = ['date_inscription', 'date_validation']
    inlines = [ParticipantSoireeInline]
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'email', 'telephone')
        }),
        ('Inscription', {
            'fields': ('nombre_personnes', 'statut', 'date_inscription', 'date_validation')
        }),
    )
    
    def statut_badge(self, obj):
        colors = {
            'en_attente': '#fbbf24',
            'valide': '#10b981',
            'refuse': '#ef4444'
        }
        labels = {
            'en_attente': '⏳ En attente',
            'valide': '✅ Validé',
            'refuse': '❌ Refusé'
        }
        color = colors.get(obj.statut, '#6b7280')
        label = labels.get(obj.statut, obj.statut)
        return mark_safe(f'<span style="background-color: {color}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold;">{label}</span>')
    statut_badge.short_description = 'Statut'
    
    actions = ['valider_inscriptions']
    
    def valider_inscriptions(self, request, queryset):
        from django.utils import timezone
        from .email_service import BrevoEmailService
        
        count = 0
        for inscription in queryset.filter(statut='en_attente'):
            inscription.statut = 'valide'
            inscription.date_validation = timezone.now()
            inscription.save()
            
            # Envoyer l'email de validation
            BrevoEmailService.send_validation_email(inscription)
            count += 1
        
        self.message_user(request, f"{count} inscription(s) validée(s) et email(s) envoyé(s).")
    valider_inscriptions.short_description = "Valider les inscriptions sélectionnées"
