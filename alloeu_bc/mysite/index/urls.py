from django.urls import path
from . import views


app_name = 'index'

urlpatterns = [
    path("", views.index, name="index"),
    path("leclub/presentations/", views.presentation, name="presentations"),
    path("leclub/informations/", views.information, name="informations"),
    path("leclub/partenaires/", views.partenaires, name="partenaires"),
    path("lesequipes/", views.lesequipes, name="lesequipes"),
    path("inscriptions/", views.inscriptions, name="inscriptions"),
    path("matchs/", views.matches, name="matches"),
    path("mentions-legales/", views.mentions_legales, name="mentions_legales"),
]