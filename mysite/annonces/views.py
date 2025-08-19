from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import strip_tags

from .forms import AnnonceForm
from .models import Annonce


def annonces_list(request):
    annonces_qs = Annonce.objects.filter(is_published=True)
    paginator = Paginator(annonces_qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "annonces/list.html", {"page_obj": page_obj})


def annonce_create(request):
    if request.method == "POST":
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.is_published = False
            annonce.save()

            # Build confirmation links
            confirm_url = request.build_absolute_uri(
                reverse("annonces:confirm", args=[annonce.publish_token])
            )
            delete_url = request.build_absolute_uri(
                reverse("annonces:delete", args=[annonce.delete_token])
            )

            subject = "Confirmez la publication de votre annonce - Alloeu Basket Club"
            html_message = (
                f"<p>Bonjour,</p>"
                f"<p>Merci pour votre annonce \"{annonce.title}\".</p>"
                f"<p>Pour la publier, cliquez sur ce lien : <a href='{confirm_url}'>Publier mon annonce</a></p>"
                f"<p>Pour la supprimer à tout moment, conservez ce lien : <a href='{delete_url}'>Supprimer mon annonce</a></p>"
                f"<p><em>Pensez à supprimer votre annonce une fois l'article vendu afin de garder la liste à jour.</em></p>"
                f"<p>Si vous perdez vos liens, contactez <a href='mailto:site.alloeubc@gmail.com'>site.alloeubc@gmail.com</a> depuis l'adresse utilisée pour l'annonce.</p>"
                f"<p>Sportivement,<br>L'équipe Alloeu Basket Club</p>"
            )
            send_mail(
                subject,
                strip_tags(html_message),
                getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@alloeubasket.fr"),
                [annonce.email],
                html_message=html_message,
            )

            return render(
                request,
                "annonces/created_pending.html",
                {"email": annonce.email},
            )
    else:
        form = AnnonceForm()

    return render(request, "annonces/create.html", {"form": form})


def confirm_publish(request, token):
    annonce = get_object_or_404(Annonce, publish_token=token)
    if not annonce.is_published:
        annonce.is_published = True
        annonce.save(update_fields=["is_published"])
    return render(request, "annonces/publish_confirmed.html", {"annonce": annonce})


def confirm_delete(request, token):
    annonce = get_object_or_404(Annonce, delete_token=token)
    title = annonce.title
    email = annonce.email
    annonce.delete()

    return render(
        request,
        "annonces/delete_confirmed.html",
        {"title": title, "email": email},
    )
