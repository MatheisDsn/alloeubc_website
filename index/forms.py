from django import forms



class InscriptionForm(forms.Form):
    last_name = forms.CharField(
        label="Nom",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "Ex: Dupont",
        }),
    )
    first_name = forms.CharField(
        label="Prénom",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "Ex: Martin",
        }),
    )
    birth_name = forms.CharField(
        label="Nom de naissance",
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
            "placeholder": "Ex : nom de jeune fille",
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
            "type": "date",
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
    
    vu_avec_coach = forms.BooleanField(
        label="J'ai déjà vu avec le coach",
        required=False, # Laisse à False si ce n'est pas strictement obligatoire pour envoyer le formulaire
        widget=forms.CheckboxInput(attrs={
            "class": "h-4 w-4 text-primary-600 border-gray-300 rounded",
        }),
    )

    surclassement = forms.BooleanField(
    label="Je souhaite un surclassement",
    required=False,
    widget=forms.CheckboxInput(attrs={
        "class": "h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500",
    }),
    )

    # MODIFICATION DE LA LIGNE "loisir"
    PARTICIPATION_CHOICES = (
        ("competition", "Jouer en compétition"),
        ("loisir", "Jouer en loisir (18 ans minimum)"), 
        ("loisir_maman", "Jouer en loisir maman"),
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
