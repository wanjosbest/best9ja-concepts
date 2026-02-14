from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, "index.html")

def services(request):
    return render(request, "services_detail.html")


def work(request):
    return render(request, "work_detail.html")


def blog(request):
    return render(request, "blog_detail.html")


def about(request):
    return render(request, "about_detail.html")

@require_POST
def newsletter_subscribe(request):
    email = request.POST.get("email")

    if not email:
        messages.error(request, "Please enter a valid email address.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email
    )

    if created:
        messages.success(
            request,
            "Thanks for subscribing! You’ll hear from us soon."
        )
    else:
        messages.info(
            request,
            "You’re already subscribed to our newsletter."
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        project_type = request.POST.get("project_type")
        message = request.POST.get("message")

        # ================= EMAIL TO YOU =================
        admin_message = f"""
New contact request from Best9ja Concepts website
Name: {name}
Email: {email}
Project Type: {project_type}
Message:
{message}
"""
        send_mail(
            subject=f"New Project Inquiry – {project_type}",
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["josephwandiyahyel3@gmail.com"],
            fail_silently=False,
        )
        # ================= AUTO REPLY TO CLIENT =================
        client_message = f"""
Hi {name},
Thank you for contacting Best9ja Concepts.
We’ve received your message regarding "{project_type}".
Our team will review it and get back to you within 24 hours (Mon–Sat).
Best regards,
Best9ja Concepts
https://best9ja.com.ng
"""
        send_mail(
            subject="We’ve received your message – Best9ja Concepts",
            message=client_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],  
            fail_silently=False,
        )
        messages.success(
            request,
            "Thank you for contacting us. We’ll get back to you within 24 hours."
        )
        return redirect("contact")
    return render(request, "contact_detail.html")