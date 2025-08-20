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
    birth_date = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={
            "type": "date",
            "class": "w-full rounded-lg border-gray-300 font-secondary focus:border-primary-500 focus:ring-primary-500",
        }),
        input_formats=["%Y-%m-%d"],
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
