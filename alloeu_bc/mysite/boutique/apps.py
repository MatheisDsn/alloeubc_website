from django.apps import AppConfig


class BoutiqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boutique'

    def ready(self):
        import boutique.signals  # Importer les signaux ici
