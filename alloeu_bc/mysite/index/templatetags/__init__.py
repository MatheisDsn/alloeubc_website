from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.filter
def safe_url(url_name):
    """
    Filtre pour générer une URL Django de manière sécurisée
    Retourne '#' si l'URL ne peut pas être résolue
    """
    if not url_name:
        return '#'
    
    try:
        return reverse(url_name)
    except (NoReverseMatch, ValueError):
        return '#'
