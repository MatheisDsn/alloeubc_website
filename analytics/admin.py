from django.contrib import admin
from django.db.models import Count
from .models import Visitor, DailyStats


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'first_visit', 'last_visit')
    list_filter = ('first_visit', 'last_visit')
    search_fields = ('ip_address',)
    readonly_fields = ('ip_address', 'first_visit', 'last_visit')
    
    def has_add_permission(self, request):
        return False


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ('date', 'unique_visitors')
    list_filter = ('date',)
    readonly_fields = ('date', 'unique_visitors')
    ordering = ('-date',)
    
    def has_add_permission(self, request):
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Ajouter le total des visiteurs depuis la création
        total_visitors = Visitor.objects.count()
        extra_context = extra_context or {}
        extra_context['total_visitors_since_creation'] = total_visitors
        return super().changelist_view(request, extra_context=extra_context)


# Personnaliser le titre de l'admin
admin.site.site_header = "Administration Alloeu BC"
admin.site.site_title = "Alloeu BC Admin"
admin.site.index_title = "Panneau d'administration"
