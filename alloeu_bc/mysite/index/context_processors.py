from .models import PartenairesSponsor

def sponsors_context(request):
    """Context processor pour rendre les sponsors disponibles sur toutes les pages"""
    return {
        'sponsors': PartenairesSponsor.objects.all()
    }
