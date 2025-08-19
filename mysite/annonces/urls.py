from django.urls import path
from . import views

app_name = "annonces"

urlpatterns = [
    path("", views.annonces_list, name="list"),
    path("nouvelle/", views.annonce_create, name="create"),
    path("confirmer/<uuid:token>/", views.confirm_publish, name="confirm"),
    path("supprimer/<uuid:token>/", views.confirm_delete, name="delete"),
]
