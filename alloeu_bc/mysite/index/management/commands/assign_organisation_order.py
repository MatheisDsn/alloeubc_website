from django.core.management.base import BaseCommand
from index.models import Organisation_card

class Command(BaseCommand):
    help = 'Assigne des ordres séquentiels aux cartes d\'organisation existantes'

    def handle(self, *args, **options):
        cards = Organisation_card.objects.all().order_by('id')
        
        for index, card in enumerate(cards):
            card.ordre = index
            card.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Carte "{card.nom} - {card.fonction}" - Ordre assigné: {card.ordre}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Ordres assignés à {cards.count()} carte(s) d\'organisation'
            )
        )
