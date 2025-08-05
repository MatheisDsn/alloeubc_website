import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # adapte si besoin
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

admin_email = "matheisdasso@gmail.com"

if not User.objects.filter(email=admin_email).exists():
    User.objects.create_superuser(
        email=admin_email,
        password="Math200815!"
    )
    print("✅ Superuser créé")
else:
    print("ℹ️ Superuser existe déjà")
