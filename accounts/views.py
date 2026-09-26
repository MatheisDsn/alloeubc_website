from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
import re

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        last_name = request.POST.get("last-name")
        first_name = request.POST.get("first-name")
        phone_number = request.POST.get("phone-number")
        password = request.POST.get("password")
        User = get_user_model()

        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number)
        user.save()
        login(request, user)
        messages.success(request, "Vous êtes bien connecté.")
        return redirect("index:index")
    else:       
        return render(request, "accounts/signup.html")

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index:index")
        else:
            messages.error(request, "Erreur : Email ou mot de passe incorrect")
            return redirect("accounts:connexion")

    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('index:index')
