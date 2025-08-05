import ast
import re
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produits, Cart, CartItem, Commande, ArticleCommande, StatutCommande
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def boutique(request):
    try:
        cart = get_object_or_404(Cart, user=request.user)
        produits_panier = CartItem.objects.filter(cart=cart)
        qtt_produits = sum(produit.quantite for produit in produits_panier)
        return render(request, 'boutique/index.html', {"produits" : Produits.objects.all(), "quantite_produits" : qtt_produits})
    except:
        qtt_produits = 0
        return render(request, 'boutique/index.html', {"produits" : Produits.objects.all(), "quantite_produits" : qtt_produits})
    
def add_to_cart_index(request, slug):
    produit = get_object_or_404(Produits, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        product=produit,
        defaults={'quantite': 1}  # Définit la quantité à 1 si c'est un nouvel item
    )

    # Si l'article existe déjà dans le panier, incrémenter la quantité
    if not item_created:
        cart_item.quantite += 1
        cart_item.save()
    return redirect('boutique:index')

def panier(request):
    try:
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = str(sum(item.product.prix * item.quantite for item in cart_items))
        return render(request, 'boutique/panier.html', {'panier': cart_items, 'prix_total': total_price})
    except:
        return render(request, 'boutique/panier.html', {'panier': None, 'prix_total': "0"})
    
def add_to_cart_cart(request, slug):
    produit = get_object_or_404(Produits, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=produit, cart=cart)
    cart_item.quantite += 1
    cart_item.save()
    return redirect('boutique:cart')


def remove_one_from_cart(request, slug):
    produit = get_object_or_404(Produits, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=produit, cart=cart)
    if cart_item.quantite > 1:
        cart_item.quantite -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('boutique:cart')

def delete_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.delete()
    return redirect('boutique:cart')
 
def remove_from_cart(request, slug):
    produit = get_object_or_404(Produits, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=produit, cart=cart)
    cart_item.delete()
    return redirect('boutique:cart')

def detail(request, slug):
    produit = get_object_or_404(Produits, slug=slug)
    try:
        cart = get_object_or_404(Cart, user=request.user)
        produits_panier = CartItem.objects.filter(cart=cart)
        qtt_produits = sum(produit.quantite for produit in produits_panier)
        return render(request, "boutique/detail.html", {"details" : produit, "quantite_produits" : qtt_produits})
    except:
        qtt_produits = 0
        return render(request, "boutique/detail.html", {"details" : produit, "quantite_produits" : qtt_produits})

def add_to_cart_details(request, slug):
    product = Produits.objects.get(slug=slug)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    cart_item.quantite += 1
    cart_item.save()
    return redirect('boutique:detail', slug)

def recapitulatif(request):
    if request.method == "POST":
        paragraphe = request.POST.get("commentaire")
        
        # Récupérer le panier de l'utilisateur
        cart = get_object_or_404(Cart, user=request.user)
        
        # Récupérer les articles du panier
        cart_items = CartItem.objects.filter(cart=cart)
        
        # Calculer le prix total
        total_price = sum(item.product.prix * item.quantite for item in cart_items)
        
        # Créer la commande et ajouter les produits commandés
        commande = Commande.objects.create(
            infos=paragraphe,
            user=request.user,
            total=total_price
        )
        
        # Ajouter les produits à la commande
        for cart_item in cart_items:
            # Créer un article de commande pour chaque item dans le panier
            ArticleCommande.objects.create(
                commande=commande,
                article=cart_item.product,
                quantite=cart_item.quantite,
                prix_article=cart_item.product.prix
            )
        
        # Vider le panier après la commande
        cart_items.delete()

        return redirect('boutique:confirmation')

    else:
        try:
            # Récupérer les articles du panier de l'utilisateur
            cart = get_object_or_404(Cart, user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            
            # Calculer le prix total
            total_price = sum(item.product.prix * item.quantite for item in cart_items)
            
            return render(request, 'boutique/recapitulatif.html', {'panier': cart_items, 'prix_total': total_price})
        
        except Cart.DoesNotExist:
            return render(request, 'boutique/panier.html', {'panier': None, 'prix_total': "0"})

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def confirmation(request):
    # Récupérer la dernière commande de l'utilisateur
    commande = Commande.objects.filter(user=request.user).latest('date_commande')
    
    # Récupérer les articles commandés associés à cette commande
    articles_commandes = ArticleCommande.objects.filter(commande=commande)

    # Préparer les détails des produits commandés
    produits = []
    for article in articles_commandes:
        produit_info = {
            'nom': article.nom_article,
            'prix': article.prix_article,
            'quantite': article.quantite,
            'image': article.article.image.url if article.article and article.article.image else None
        }
        produits.append(produit_info)

    # Préparer les données pour les emails
    c = {
        'first_name': request.user.first_name, 
        'last_name': request.user.last_name, 
        "commande": commande, 
        "produits": produits
    }

    # Générer le contenu des emails
    text_content = render_to_string('boutique/email_templates/email_recap_user.txt', c)
    html_content = render_to_string('boutique/email_templates/email_recap_user.html', c)

    # Envoyer l'email de confirmation à l'utilisateur
    email = EmailMultiAlternatives('CONFIRMATION DE RÉSERVATION', text_content)
    email.attach_alternative(html_content, "text/html")
    email.to = [request.user.email]  # Utilise l'email au lieu du username pour l'envoi
    email.send()

    # Envoyer un email à l'administrateur
    c2 = c  # Les données sont similaires pour l'email admin
    text_content2 = render_to_string('boutique/email_templates/email_recap_admin.txt', c2)
    html_content2 = render_to_string('boutique/email_templates/email_recap_admin.html', c2)

    email2 = EmailMultiAlternatives('NOUVELLE COMMANDE DEPUIS LE SITE WEB', text_content2)
    email2.attach_alternative(html_content2, "text/html")
    email2.to = ['matheisdasso@gmail.com']  # Email de l'admin
    email2.send()

    # Afficher la page de confirmation
    return render(request, 'boutique/confirmation.html', {
        'numero_commande': commande.numero_commande,
        "date_commande": commande.date_commande,
        "total": commande.total,
        "produits": produits
    })


def commandes(request):
    commandes = Commande.objects.filter(user=request.user)
    return render(request, 'boutique/commandes.html', {"commandes" : commandes})

def detail_commande(request, id):
    commande = get_object_or_404(Commande, user=request.user, id=id)
    articles_commandes = ArticleCommande.objects.filter(commande=commande)

    # Préparer les informations des produits avec tous les détails nécessaires
    produits_details = []
    for article in articles_commandes:
        produit_info = {
            'nom': article.nom_article,
            'prix': article.prix_article,
            'quantite': article.quantite,
            'image': article.article.image.url if article.article and article.article.image else None  # Récupérer l'image si le produit existe
        }
        produits_details.append(produit_info)

    return render(request, 'boutique/detail_commande.html', {"produits": produits_details, "commande": commande})


def profil(request):
    return render(request, "boutique/profil.html", {"user": request.user})

def modifier_profil(request):
    if request.method == "POST":
        user = request.user  # Récupérer l'utilisateur actuellement authentifié
        if request.POST.get("username"):
            if not bool(re.match(r'[^@]+@[^@]+\.[^@]+', request.POST.get("username"))):
                messages.error(request, "Erreur : Votre adresse mail est incorrecte.")
                return redirect("boutique:profil_edit")
            else:
                user.username = request.POST.get("username")
        if request.POST.get("last-name"):
            user.last_name = request.POST.get("last-name")
        if request.POST.get("first-name"):
            user.first_name = request.POST.get("first-name")
        if request.POST.get("phone-number"):
            if not bool(re.match(r'^(?:\+?33|0)(?:[7]|6|3|9)\d{8}$', request.POST.get("phone-number"))):
                messages.error(request, "Erreur : Votre numéro de téléphone est incorrect")
                return redirect("boutique:profil_edit")
            else:
                user.phone_number = request.POST.get("phone-number")
        if request.POST.get("password"):
            if len(request.POST.get("password")) < 10:
                messages.error(request, "Erreur : Votre mot de passe doit contenir au moins 10 caractères.")
                return redirect("boutique:profil_edit")
            else:
                user.set_password(request.POST.get("password"))
        user.save()
        return redirect("boutique:profil")
    else:
        return render(request, 'boutique/modifier_profil.html', {"user": request.user})
    
def modifier_mdp(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        user = request.user

        # Vérifier que l'ancien mot de passe est correct
        if not user.check_password(old_password):
            messages.error(request, "L'ancien mot de passe est incorrect.")
            return redirect("boutique:mdp_edit")
            # Vérifier que les deux nouveaux mots de passe correspondent
        elif new_password1 != new_password2:
            messages.error(request, "Erreur : Les nouveaux mots de passe ne correspondent pas.")
            return redirect("boutique:mdp_edit")
        elif len(new_password1) < 10:
            messages.error(request, "Erreur : Votre mot de passe doit contenir au moins 10 caractères.")
            return redirect("boutique:mdp_edit")
        # Le mot de passe doit contenir au moins une lettre minuscule.
        elif not re.search("[a-z]", new_password1):
            messages.error(request, "Erreur : Votre mot de passe doit contenir au moins une lettre minuscule.")
            return redirect("boutique:mdp_edit")
        else:
            user.set_password(new_password1)
            user.save()
            messages.success(request, "Votre mot de passe à été modifié avec succès, vous avez été déconnecté, veuillez vous reconnecter avec votre nouveau mot de passe.")
            return redirect("boutique:produits")  # Rediriger vers la page du profil après la modification du mot de passe
    else:
        return render(request, 'boutique/modifier_mdp.html')
    
@receiver(post_save, sender=Commande)
def envoyer_email_changement_statut(sender, instance, **kwargs):
    if instance.statut == StatutCommande.PRETE:
        commande = Commande.objects.filter(user=instance.user).latest('date_commande')
        produits = ast.literal_eval(commande.produits_commandes)

        c = {'first_name': instance.user.first_name, 'last_name': instance.user.last_name, "commande": commande, "produits": produits}

        text_content = render_to_string('boutique/email_templates/email.txt', c)
        html_content = render_to_string('boutique/email_templates/email.html', c)

        email = EmailMultiAlternatives('Votre commande est disponible ! - AlloeuBC', text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = [instance.user.username]
        email.send()

