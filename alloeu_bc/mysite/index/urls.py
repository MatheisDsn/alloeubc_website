from django.urls import path
from . import views


app_name = 'index'

urlpatterns = [
    path("", views.index, name="index"),
    path("leclub/presentations/", views.presentation, name="presentations"),
    path("leclub/informations/", views.information, name="informations"),
    path("leclub/partenaires/", views.partenaires, name="partenaires"),
    path("inscriptions/", views.inscriptions, name="inscriptions"),
    path("lesequipes/", views.lesequipes, name="lesequipes"),
    path("matchs/", views.matches, name="matches"),
    path("mentions-legales/", views.mentions_legales, name="mentions_legales"),
    
    # URLs pour la soirée festive
    path("inscription-soiree/", views.inscription_soiree, name="inscription_soiree"),
    path("inscription-soiree/success/", views.inscription_soiree_success, name="inscription_soiree_success"),
    path("admin-soiree/", views.admin_soiree, name="admin_soiree"),
    path("admin-soiree/valider/<int:inscription_id>/", views.valider_inscription, name="valider_inscription"),
    path("admin-soiree/refuser/<int:inscription_id>/", views.refuser_inscription, name="refuser_inscription"),
]
