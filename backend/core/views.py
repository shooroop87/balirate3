from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import path


def index(request):
    """Главная страница."""
    from subscriptions.models import Plan
    from blog.models import BlogPost
    
    plans = Plan.objects.filter(is_active=True).order_by("price")
    
    latest_posts = BlogPost.objects.filter(
        status=BlogPost.Status.PUBLISHED
    ).select_related("category").order_by("-published_at")[:3]
    
    return render(request, "pages/index.html", {
        "plans": plans,
        "latest_posts": latest_posts,
    })


def how_it_works(request):
    """Как это работает."""
    return render(request, "pages/how_it_works.html")


def pricing(request):
    """Страница с тарифами."""
    from subscriptions.models import Plan
    plans = Plan.objects.filter(is_active=True).order_by("price")
    return render(request, "pages/pricing.html", {"plans": plans})


def faq(request):
    """Часто задаваемые вопросы."""
    faqs = [
        {
            "question": _("Was ist ein Blister?"),
            "answer": _("Ein Blister ist eine vorportionierte Verpackung Ihrer Medikamente, sortiert nach Einnahmezeitpunkt (morgens, mittags, abends, nachts). So wissen Sie immer genau, welche Tabletten Sie wann nehmen müssen.")
        },
        {
            "question": _("Wer prüft meine Medikamente?"),
            "answer": _("Alle Medikamente werden von qualifizierten Apothekern unserer Partnerapotheken geprüft. Dabei achten wir auf Wechselwirkungen, Dosierung und Eignung für die Verblisterung.")
        },
        {
            "question": _("Wie oft erhalte ich meine Lieferung?"),
            "answer": _("Sie können zwischen 7, 14 oder 28 Tagen Lieferintervall wählen. Die Lieferung erfolgt immer rechtzeitig vor Ablauf Ihrer aktuellen Blister.")
        },
        {
            "question": _("Brauche ich ein Rezept?"),
            "answer": _("Für rezeptpflichtige Medikamente benötigen wir ein gültiges Rezept von Ihrem Arzt. Dieses können Sie als Foto/Scan hochladen oder per Post einsenden.")
        },
        {
            "question": _("Kann ich mein Abonnement pausieren?"),
            "answer": _("Ja, Sie können Ihr Abonnement jederzeit für bis zu 3 Monate pausieren, z.B. bei einem Krankenhausaufenthalt oder Urlaub.")
        },
        {
            "question": _("Wohin wird geliefert?"),
            "answer": _("Wir liefern nach ganz Deutschland und Österreich. Die Lieferung erfolgt durch DHL mit Sendungsverfolgung.")
        },
    ]
    return render(request, "pages/faq.html", {"faqs": faqs})


def contact(request):
    """Kontaktseite."""
    if request.method == "POST":
        # TODO: Kontaktformular verarbeiten
        pass
    return render(request, "pages/contact.html")


@login_required
def dashboard(request):
    """Benutzer-Dashboard."""
    user = request.user
    
    # Aktive Subscription
    subscription = user.subscriptions.filter(
        status__in=["active", "trialing"]
    ).first()
    
    # Letzte Bestellungen
    recent_orders = user.balirate_orders.order_by("-created_at")[:5]
    
    # Aktive Medikamente
    medications = user.medications.filter(is_active=True)
    
    context = {
        "subscription": subscription,
        "recent_orders": recent_orders,
        "medications": medications,
    }
    return render(request, "pages/dashboard.html", context)


@require_POST
def submit_review(request):
    """Отправка отзыва на почту админа."""
    name = request.POST.get('name')
    email = request.POST.get('email')
    rating = request.POST.get('rating')
    message = request.POST.get('message')
    
    subject = f"Neue Bewertung von {name} ({rating}★)"
    body = f"""
Neue Bewertung eingegangen:

Name: {name}
E-Mail: {email}
Bewertung: {rating} Sterne

Nachricht:
{message}
"""
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],  # На админскую почту
        fail_silently=True,
    )
    
    messages.success(request, _("Vielen Dank für Ihre Bewertung!"))
    return redirect('index')

def privacy(request):
    """Datenschutzerklärung."""
    return render(request, "pages/privacy.html")


def terms(request):
    """AGB."""
    return render(request, "pages/terms.html")


def imprint(request):
    """Impressum."""
    return render(request, "pages/imprint.html")


def withdrawal(request):
    """Widerrufsbelehrung."""
    return render(request, "pages/withdrawal.html")


def consent(request):
    """Patienteneinwilligung."""
    return render(request, "pages/consent.html")


def cookies(request):
    """Cookie-Einstellungen."""
    return render(request, "pages/cookies.html")