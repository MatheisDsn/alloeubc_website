from django.urls import path
from . import views

app_name = 'boutique'

urlpatterns = [
    path("", views.boutique, name="index"),
    path("<str:slug>", views.detail, name="detail"),
    path("panier/", views.panier, name="cart"),
    path("commande/", views.commandes, name="commande"),
    path("detail_commande/n_<str:id>", views.detail_commande, name="detail_commande"),
    path("profil/", views.profil, name="profil"),
    path("profil/edit", views.modifier_profil, name="profil_edit"),
    path("profil/edit/mot_de_passe", views.modifier_mdp, name="mdp_edit"),
    path("add_to_card_details/<str:slug>/", views.add_to_cart_details, name="add_to_card_details"),
    path("add_to_card_index/<str:slug>", views.add_to_cart_index, name="add_to_card_index"),
    path("add_to_card_card/<str:slug>", views.add_to_cart_cart, name="add_to_card_card"),
    path("remove_one_from_cart/<str:slug>", views.remove_one_from_cart, name="remove_one_from_cart"),
    path("panier/delete", views.delete_cart, name="delete_cart"),
    path("panier/delete/<str:slug>", views.remove_from_cart, name="delete_product"),
    path("panier/recapitulatif", views.recapitulatif, name="recap"),
    path("panier/confirmation", views.confirmation, name="confirmation"),
]