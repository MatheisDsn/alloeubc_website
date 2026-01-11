from django import forms


class InscriptionSoireeForm(forms.Form):
    """Formulaire d'inscription à la soirée festive"""
    nom = forms.CharField(
        label="Nom",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "Votre nom",
        }),
    )
    prenom = forms.CharField(
        label="Prénom",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "Votre prénom",
        }),
    )
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "votre.email@example.com",
        }),
    )
    telephone = forms.CharField(
        label="Numéro de téléphone",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "06 12 34 56 78",
        }),
    )
    nombre_personnes = forms.IntegerField(
        label="Nombre de personnes à inscrire",
        min_value=1,
        max_value=20,
        initial=1,
        widget=forms.NumberInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "min": "1",
            "max": "20",
        }),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Récupérer le nombre de personnes depuis les données POST ou initial
        nombre = self.data.get('nombre_personnes') if self.data else None
        if nombre is None and self.initial:
            nombre = self.initial.get('nombre_personnes', 1)
        if nombre is None:
            nombre = 1
        
        try:
            nombre = int(nombre)
        except (ValueError, TypeError):
            nombre = 1
        
        # Créer dynamiquement les champs pour chaque participant
        for i in range(1, nombre + 1):
            self.fields[f'lien_club_{i}'] = forms.CharField(
                label=f"Lien avec le club - Personne {i}",
                max_length=200,
                widget=forms.TextInput(attrs={
                    "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
                    "placeholder": "Ex: Joueur, Parent, Entraîneur, Bénévole...",
                }),
                help_text="Précisez le lien de cette personne avec le club"
            )


class InscriptionForm(forms.Form):
    full_name = forms.CharField(
        label="Nom et prénom",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "Ex: Martin Dupont",
        }),
    )
    sexe = forms.ChoiceField(
        label="Sexe",
        choices=[("M", "Masculin"), ("F", "Féminin"), ("A", "Autre")],
        widget=forms.Select(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
        }),
    )
    birth_date = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(format="%d/%m/%Y", attrs={
            "type": "date",  # HTML5 date input utilise toujours YYYY-MM-DD en interne
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
        }),
    )
    email = forms.EmailField(
        label="Adresse mail",
        widget=forms.EmailInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "nom@example.com",
        }),
    )
    phone = forms.CharField(
        label="N° de téléphone",
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "+33 6 12 34 56 78",
        }),
    )
    licensed_before = forms.BooleanField(
        label="J'ai déjà été licencié(e)",
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "h-4 w-4 text-primary-600 border-gray-300 rounded",
        }),
    )

    PARTICIPATION_CHOICES = (
        ("competition", "Jouer en compétition"),
        ("loisir", "Jouer en loisir"),
        ("entrainer", "Entraîner une équipe"),
        ("arbitrer", "Arbitrer"),
        ("officier", "Officier hors arbitrage"),
        ("diriger", "Diriger"),
        ("adherent", "Être uniquement adhérent au club"),
    )

    participation_roles = forms.MultipleChoiceField(
        label="Souhait(s) au club",
        required=False,
        choices=PARTICIPATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Vous pouvez en choisir plusieurs",
    )
