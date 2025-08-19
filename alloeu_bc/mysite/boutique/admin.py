from django.contrib import admin
from boutique.models import Produits, Cart, CartItem, Commande, ArticleCommande
from accounts.models import User

class ProduitsAdmin(admin.ModelAdmin):
    exclude = ['slug'] 
    list_display = ("nom", "prix", "description_principal")


class CommandeArticleInline(admin.TabularInline):
    model = ArticleCommande
    extra = 1
    readonly_fields = ["nom_article", "prix_article"]

    def nom_du_produit(self, obj):
        if obj.article:
            return obj.article.nom
        return obj.nom_article  # Utiliser le nom sauvegardé si le produit n'existe plus

    def prix_du_produit(self, obj):
        if obj.article:
            return obj.article.prix
        return obj.prix_article  # Utiliser le prix sauvegardé si le produit n'existe plus

    nom_du_produit.short_description = "Nom du produit"
    prix_du_produit.short_description = "Prix du produit"

class CommandeAdmin(admin.ModelAdmin):
    inlines = [CommandeArticleInline]
    list_display = ("commande", "utilisateur", "date", "statut")
    readonly_fields = ["total", "numero_commande"]
    
    def commande(self, obj):
        return f"Commande n°{obj.id}"
    
    def utilisateur(self, obj):
        return f"Utilisateur : {obj.user}"
    
    def date(self, obj):
        return f"Date de commande : {obj.date_commande}"



class PanierArticleInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('product', 'prix')
    fields = ("product", "prix", 'quantite')

    def prix(self, obj):
        return obj.product.prix 
    
class PanierAdmin(admin.ModelAdmin):
    inlines = [PanierArticleInline]
    list_display = ['user', 'date_creation']
    def has_add_permission(self, request):
        # Retourner False pour désactiver la possibilité d'ajouter un nouveau panier
        return False


admin.site.register(Produits, ProduitsAdmin)
admin.site.register(Cart, PanierAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(User)