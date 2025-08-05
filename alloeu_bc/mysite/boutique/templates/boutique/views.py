from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
import re

def signup(requests):
    if requests.method == "POST":
        username = requests.POST.get("username")
        last_name = requests.POST.get("last-name")
        first_name = requests.POST.get("first-name")
        phone_number = requests.POST.get("phone-number")
        password = requests.POST.get("password")
        new_password2 = requests.POST.get("new_password2")
        User = get_user_model()

        if not bool(re.match(r'^(?:\+?33|0)(?:[7]|6|3|9)\d{8}$', phone_number)):
            messages.error(requests, "Erreur : Votre numéro de téléphone est incorrect")
            return redirect("accounts:inscription")
        elif len(password) < 10:
            messages.error(requests, "Erreur : Votre mot de passe doit contenir au moins 10 caractères.")
            return redirect("accounts:inscription")
        elif password != new_password2:
            messages.error(requests, "Erreur : Les deux mots de passe ne correspondent pas.")
            return redirect("accounts:inscription")
        elif not bool(re.match(r'[^@]+@[^@]+\.[^@]+', username)):
            messages.error(requests, "Erreur : Votre adresse mail est incorrecte.")
            return redirect("accounts:inscription")
        else:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.phone_number = phone_number
            user.save()
            login(requests, user)
            messages.success(requests, "Vous êtes bien connecté.")
            return redirect("boutique:produits")
    else:       
        return render(requests, "accounts/signup.html")

def login_user(requests):
    if requests.method == "POST":
        username = requests.POST.get("username")
        password = requests.POST.get("password")
        user = authenticate(requests, username=username, password=password)

        if user is not None:
            login(requests, user)
            return redirect("boutique:produits")
        else:
            messages.error(requests, "Erreur : Email ou mot de passe incorrect")
            return redirect("accounts:connexion")

    return render(requests, 'accounts/login.html')

def logout_user(requests):
    logout(requests)
    return redirect('boutique:produits')