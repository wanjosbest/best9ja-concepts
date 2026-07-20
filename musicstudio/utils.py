from django.core.mail import send_mail
from django.conf import settings


def send_purchase_email(request, purchase):

    subject = f"Your Beat Purchase - {purchase.beat.title}"

    # Full URL generation
    download_link = request.build_absolute_uri(
        purchase.beat.audio.url
    )

    message = f"""
Hi,

Thank you for purchasing "{purchase.beat.title}" from Best9ja Concepts.

Download your beat below:

{download_link}

Enjoy your music journey.

- Best9ja Concepts
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [purchase.email],
        fail_silently=False,
    )