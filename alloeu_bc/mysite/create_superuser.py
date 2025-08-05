import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # modifie si ton settings est ailleurs
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "matheisdasso@gmail.com", "Math200815!")
    print("✅ Superuser créé")
else:
    print("ℹ️ Superuser existe déjà")
