# models.py

from django.db import models
from django.utils.text import slugify
from django.conf import settings


class BeatCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Beat(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BeatCategory, on_delete=models.CASCADE, related_name="beats")
    image = models.ImageField(upload_to="beats/images/")
    audio = models.FileField(upload_to="beats/audio/")
    bpm = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    message = models.TextField()

    def __str__(self):
        return self.name


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases", null=True)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.user.email}- {self.beat.title}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email