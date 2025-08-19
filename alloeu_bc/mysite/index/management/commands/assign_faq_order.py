from django.core.management.base import BaseCommand
from index.models import FAQ

class Command(BaseCommand):
    help = 'Assigne des ordres séquentiels aux FAQ existantes'

    def handle(self, *args, **options):
        faqs = FAQ.objects.all().order_by('id')
        
        for index, faq in enumerate(faqs):
            faq.ordre = index
            faq.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'FAQ "{faq.question}" - Ordre assigné: {faq.ordre}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Ordres assignés à {faqs.count()} FAQ(s)'
            )
        )
