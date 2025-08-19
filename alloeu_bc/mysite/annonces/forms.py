from django import forms
from .models import Annonce


class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = [
            "title",
            "description",
            "category",
            "image",
            "email",
            "phone",
            "price",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-secondary-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500", "placeholder": "Titre de l'annonce"}),
            "description": forms.Textarea(attrs={"class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-secondary-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500", "rows": 5, "placeholder": "Description"}),
            "category": forms.Select(attrs={"class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-secondary-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"}),
            "email": forms.EmailInput(attrs={"class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-secondary-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500", "placeholder": "Votre adresse mail"}),
            "phone": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-secondary-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500", "placeholder": "Votre numéro (facultatif)"}),
            "price": forms.NumberInput(attrs={"class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-secondary-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500", "placeholder": "Prix en €", "min": "0", "step": "0.01"}),
        }
