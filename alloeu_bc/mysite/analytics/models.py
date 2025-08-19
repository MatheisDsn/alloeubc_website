from django.db import models
from django.utils import timezone


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    first_visit = models.DateTimeField(default=timezone.now)
    last_visit = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Visiteur"
        verbose_name_plural = "Visiteurs"
    
    def __str__(self):
        return f"{self.ip_address} - Première visite: {self.first_visit.strftime('%d/%m/%Y')}"


class DailyStats(models.Model):
    date = models.DateField(unique=True)
    unique_visitors = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Statistique journalière"
        verbose_name_plural = "Statistiques journalières"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date} - {self.unique_visitors} visiteurs"