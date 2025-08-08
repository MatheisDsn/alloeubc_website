from django.core.management.base import BaseCommand
from news.models import Article


class Command(BaseCommand):
    help = 'Teste le calcul du temps de lecture des articles'

    def handle(self, *args, **options):
        articles = Article.objects.all()
        
        self.stdout.write('=== Test du temps de lecture ===')
        
        for article in articles:
            word_count = len(article.content.split())
            calculated_time = max(1, round(word_count / 200))
            
            self.stdout.write(f'\nArticle: {article.title}')
            self.stdout.write(f'Nombre de mots: {word_count}')
            self.stdout.write(f'Temps calculé: {calculated_time} min')
            self.stdout.write(f'Property reading_time: {article.reading_time} min')
            self.stdout.write(f'Contenu (premiers 100 caractères): {article.content[:100]}...')
            self.stdout.write('-' * 50)
