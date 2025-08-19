from django.contrib import admin
from .models import Annonce


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "email", "phone", "is_published", "created_at")
    list_filter = ("is_published", "category", "created_at")
    search_fields = ("title", "description", "email", "phone")
    readonly_fields = ("publish_token", "delete_token", "created_at")
