from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import Visitor, DailyStats
from datetime import date


class AnalyticsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Obtenir l'IP du visiteur
        ip_address = self.get_client_ip(request)
        today = date.today()
        
        # Créer ou récupérer le visiteur (un visiteur unique par IP)
        visitor, created = Visitor.objects.get_or_create(
            ip_address=ip_address,
            defaults={
                'first_visit': timezone.now(),
                'last_visit': timezone.now(),
            }
        )
        
        # Si le visiteur existe déjà, mettre à jour sa dernière visite
        if not created:
            visitor.last_visit = timezone.now()
            visitor.save()
        
        # Mettre à jour les statistiques quotidiennes
        daily_stats, created = DailyStats.objects.get_or_create(
            date=today,
            defaults={'unique_visitors': 0}
        )
        
        # Si c'est un nouveau visiteur aujourd'hui, l'ajouter aux stats
        if not Visitor.objects.filter(
            ip_address=ip_address,
            last_visit__date=today
        ).exclude(id=visitor.id).exists():
            daily_stats.unique_visitors += 1
            daily_stats.save()
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
