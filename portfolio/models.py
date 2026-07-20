from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse

class User(AbstractUser):
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.email
































        
    
class Upload_Image(models.Model):
    image = models.ImageField(upload_to="images")
   
    
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
class Blog_Post(models.Model):
    user = models.ForeignKey(User, related_name="blog_post_user",on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    meta_keywords = models.CharField(max_length=100)
    meta_descriptions = models.CharField(max_length=250)
    featured_image = models.ImageField(upload_to = "images", null=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return f" {self.user} added {self.title}"

    

class Service(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=10, blank=True, help_text="Emoji icon e.g 💻")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    client_name = models.CharField(max_length=200, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    technologies = models.CharField(
        max_length=255,
        help_text="Comma separated e.g Django, React, AWS"
    )
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    message = models.TextField()
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.company}"