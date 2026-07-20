# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, login
from .models import Beat, BeatCategory, Testimonial, Purchase
import uuid
import requests
from django.conf import settings
from .utils import send_purchase_email

User = get_user_model()


def home(request):
    beats = Beat.objects.select_related("category").all().order_by("-created_at")
    featured_beats = Beat.objects.filter(is_featured=True)[:3]
    categories = BeatCategory.objects.all()
    testimonials = Testimonial.objects.all()

    context = {
        "beats": beats,
        "featured_beats": featured_beats,
        "categories": categories,
        "testimonials": testimonials,
    }

    return render(request, "music/music_index.html", context)


def checkout(request, slug):
    beat = get_object_or_404(Beat, slug=slug)

    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            return render(request, "music/checkout.html", {
                "beat": beat,
                "error": "Email is required"
            })

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email
            }
        )

        reference = str(uuid.uuid4())

        purchase = Purchase.objects.create(
            user=user,
            beat=beat,
            reference=reference,
            amount=beat.price,
            paid=False
        )

        url = f"{settings.PAYSTACK_BASE_URL}/transaction/initialize"

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": user.email,
            "amount": int(beat.price * 100),
            "reference": reference,
            "callback_url": request.build_absolute_uri("/payment/verify/")
        }

        response = requests.post(url, json=data, headers=headers)
        result = response.json()

        if result.get("status"):
            return redirect(result["data"]["authorization_url"])

        return render(request, "music/checkout.html", {
            "beat": beat,
            "error": "Payment initialization failed. Try again."
        })

    return render(request, "music/checkout.html", {"beat": beat})


def verify_payment(request):
    reference = request.GET.get("reference")

    if not reference:
        return redirect("/")

    url = f"{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    if result["data"]["status"] == "success":
        try:
            purchase = Purchase.objects.get(reference=reference)

            if not purchase.paid:
                purchase.paid = True
                purchase.save()

                login(request, purchase.user)

                send_purchase_email(request, purchase)

            return redirect("success", reference=reference)

        except Purchase.DoesNotExist:
            return redirect("/")

    return redirect("/")


def success(request, reference):
    purchase = get_object_or_404(Purchase, reference=reference, paid=True)

    return render(request, "music/success.html", {
        "purchase": purchase
    })


def category_beats(request, pk):
    category = get_object_or_404(BeatCategory, pk=pk)

    beats = Beat.objects.filter(category=category).order_by("-created_at")

    context = {
        "category": category,
        "beats": beats,
    }

    return render(request, "music/category.html", context)