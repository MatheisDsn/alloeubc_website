from django.core.management.base import BaseCommand
from analytics.utils import calculate_monthly_stats


class Command(BaseCommand):
    help = 'Calcule les statistiques mensuelles'

    def handle(self, *args, **options):
        stats = calculate_monthly_stats()
        if stats:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Statistiques mensuelles calculées pour {stats.month:02d}/{stats.year}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('Aucune donnée à traiter')
            )
