from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import CartItem, Cart

# Signal pour vérifier après la suppression d'un CartItem
@receiver(post_delete, sender=CartItem)
def delete_cart_if_empty(sender, instance, **kwargs):
    try:
        cart = instance.cart
        # Vérifie si le panier n'a plus d'articles
        if not cart.cartitem_set.exists():
            cart.delete()  # Supprime le panier si aucun article n'y reste
    except Cart.DoesNotExist:
        # Si le panier n'existe plus, on passe
        pass
