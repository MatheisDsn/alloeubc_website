from django import forms


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

    participation_role = forms.ChoiceField(
        label="Souhait au club",
        required=False,
        choices=PARTICIPATION_CHOICES,
        widget=forms.Select(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
        }),
        help_text="Choisissez une option",
    )
