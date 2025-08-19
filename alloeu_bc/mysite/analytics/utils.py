import re
import requests
from django.conf import settings


def get_device_type(user_agent):
    """
    Détermine le type d'appareil basé sur le user agent
    """
    user_agent = user_agent.lower()
    
    # Détecter les mobiles
    mobile_patterns = [
        r'mobile', r'android', r'iphone', r'ipod', r'blackberry', 
        r'windows phone', r'palm', r'symbian'
    ]
    
    # Détecter les tablettes
    tablet_patterns = [
        r'ipad', r'tablet', r'kindle', r'playbook', r'nexus (?:[0-9]+)'
    ]
    
    for pattern in tablet_patterns:
        if re.search(pattern, user_agent):
            return 'tablet'
    
    for pattern in mobile_patterns:
        if re.search(pattern, user_agent):
            return 'mobile'
    
    return 'desktop'


def get_location_from_ip(ip_address):
    """
    Obtient la géolocalisation à partir de l'adresse IP
    Utilise ipapi.co (gratuit, 1000 requêtes/jour)
    """
    if ip_address in ['127.0.0.1', '::1'] or ip_address.startswith('192.168.'):
        return {'country': 'Local', 'city': 'Local'}
    
    try:
        response = requests.get(
            f'https://ipapi.co/{ip_address}/json/',
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return {
                'country': data.get('country_name', 'Inconnu'),
                'city': data.get('city', 'Inconnu')
            }
    except requests.RequestException:
        pass
    
    return None


def calculate_monthly_stats():
    """
    Calcule les statistiques mensuelles à partir des données journalières
    """
    from .models import DailyStats, MonthlyStats
    from django.db.models import Sum, Avg
    from datetime import datetime
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Obtenir les statistiques du mois actuel
    monthly_data = DailyStats.objects.filter(
        date__month=current_month,
        date__year=current_year
    ).aggregate(
        total_unique=Sum('unique_visitors'),
        total_visits=Sum('total_visits'),
        total_mobile=Sum('mobile_visits'),
        total_desktop=Sum('desktop_visits'),
        total_tablet=Sum('tablet_visits'),
        avg_time=Avg('average_time_spent')
    )
    
    if monthly_data['total_visits']:
        total_visits = monthly_data['total_visits']
        mobile_percentage = (monthly_data['total_mobile'] or 0) / total_visits * 100
        desktop_percentage = (monthly_data['total_desktop'] or 0) / total_visits * 100
        tablet_percentage = (monthly_data['total_tablet'] or 0) / total_visits * 100
        
        # Créer ou mettre à jour les statistiques mensuelles
        monthly_stats, created = MonthlyStats.objects.get_or_create(
            year=current_year,
            month=current_month,
            defaults={
                'unique_visitors': monthly_data['total_unique'] or 0,
                'total_visits': total_visits,
                'mobile_percentage': mobile_percentage,
                'desktop_percentage': desktop_percentage,
                'tablet_percentage': tablet_percentage,
                'average_time_spent': monthly_data['avg_time'] or 0
            }
        )
        
        if not created:
            monthly_stats.unique_visitors = monthly_data['total_unique'] or 0
            monthly_stats.total_visits = total_visits
            monthly_stats.mobile_percentage = mobile_percentage
            monthly_stats.desktop_percentage = desktop_percentage
            monthly_stats.tablet_percentage = tablet_percentage
            monthly_stats.average_time_spent = monthly_data['avg_time'] or 0
            monthly_stats.save()
        
        return monthly_stats
    
    return None
