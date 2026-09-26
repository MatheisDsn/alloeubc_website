from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("inscription", views.signup, name="inscription"),
    path("connexion", views.login_user, name="connexion"),
    path("deconnexion", views.logout_user, name="deconnexion"),
]