from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber
from django.core.mail import send_mail
from django.conf import settings
from .models import (Blog_Post,Service,Project, Testimonial)
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
import re
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method =="POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        address = request.POST.get("address")

        if confirm_password != password:
            messages.error(request, "Password Mismatched")
            return redirect("register")
    
        if not re.search(r"[A-Z]", password):
           messages.error(request, "password must contain UpperCase")
           return redirect("register")
        
        if not re.search(r"[a-z]", password):
           messages.error(request, "password must contain LowerCase")
           return redirect("register")
        
        if not re.search(r"\d", password):
           messages.error(request, "password must contain Number")
           return redirect("register")
        
        if not re.search(r"[!@#$%^&*()_+-=[\"']:|,<.>/?]", password):
            messages.error(request, "Password Must Contain Special Characters")
            return redirect("register")
        
        saveuser = User.objects.create(email = email, username = username, password = password, address = address)
        saveuser.save()
        messages.success(request, "User Registered Successfully")
        return redirect("/")
    return render(request, "account/register.html")

def home(request):
    services = Service.objects.all()[:6]    
    projects = Project.objects.all()[:6]
    posts = Blog_Post.objects.all()[:3]
    testi = Testimonial.objects.all()[:3]

    context = {
        "services": services,
        "projects": projects,
        "posts": posts,
        "testi":testi,
    }

    return render(request, "index.html", context)



def services_list(request):
    services = Service.objects.all()
    return render(request, "services/services_list.html", {"services": services})

# DETAIL
def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, "services/service_detail.html", {"service": service})

# CREATE
@login_required()
def create_service(request):
    if request.method == "POST":
        title = request.POST.get("title")
        short_description = request.POST.get("short_description")
        description = request.POST.get("description")
        icon = request.POST.get("icon")
        image = request.FILES.get("image")

        if Service.objects.filter(title__iexact=title).exists():
            messages.error(request, "Service already exists")
            return redirect("create_service")
        Service.objects.create(
            title=title,
            short_description=short_description,
            description=description,
            icon=icon,
            image=image
        )
        messages.success(request, "Service created successfully")
        return redirect("services_list")

    return render(request, "services/create_service.html")


# UPDATE
@login_required()
def update_service(request, slug):
    service = get_object_or_404(Service, slug=slug)
    if request.method == "POST":
        service.title = request.POST.get("title")
        service.short_description = request.POST.get("short_description")
        service.description = request.POST.get("description")
        service.icon = request.POST.get("icon")

        if request.FILES.get("image"):
            service.image = request.FILES.get("image")
        service.save()
        messages.success(request, "Service updated successfully")
        return redirect(service.get_absolute_url())

    return render(request, "services/update_service.html", {"service": service})


# DELETE
@login_required()
def delete_service(request, slug):
    service = get_object_or_404(Service, slug=slug)

    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted")
        return redirect("services_list")
    return render(request, "services/delete_service.html", {"service": service})


def work(request):
    return render(request, "work_detail.html")

@login_required
def create_blog_post_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        featured_image = request.FILES.get("featured_image")
        meta_keywords = request.POST.get("meta_keywords")
        meta_descriptions = request.POST.get("meta_descriptions")

        if Blog_Post.objects.filter(title__iexact=title).exists():
            messages.error(request, "Title already exists. Use another one.")
            return redirect("create_blog_post")

        post = Blog_Post.objects.create(
            user=request.user,
            title=title,
            content=content,
            featured_image=featured_image,
            meta_keywords=meta_keywords,
            meta_descriptions=meta_descriptions,
            slug=slugify(title)
        )

        messages.success(request, "Post created successfully.")
        return redirect("blog_details", slug=post.slug)

    return render(request, "blog/create_blog_post.html")
# blog lists
def blog_post_list_view(request):
    blog = Blog_Post.objects.all().order_by("-created")
    return render(request, "blog/blog_post_list.html", {"blog": blog})

#blog details
def blog_post_details_view(request, slug):
    post = get_object_or_404(Blog_Post, slug=slug)
    return render(request, "blog/blog_details.html", {"post": post})

# update post 

@login_required()
def update_blog_post_view(request, slug):
    post = get_object_or_404(Blog_Post, slug=slug)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.meta_keywords = request.POST.get("meta_keywords")
        post.meta_descriptions = request.POST.get("meta_descriptions")

        if request.FILES.get("featured_image"):
            post.featured_image = request.FILES.get("featured_image")

        post.slug = slugify(post.title)
        post.save()

        messages.success(request, "Post updated successfully.")
        return redirect("blog_details", slug=post.slug)

    return render(request, "blog/blog_post_update.html", {"post": post})

#delete blog posts 
@login_required()
def delete_blog_post_view(request, slug):
    post = get_object_or_404(Blog_Post, slug=slug)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect("blog_list")

    return render(request, "blog/delete_blog_post.html", {"post": post})
def blog(request):
    return render(request, "blog_detail.html")


def about(request):
    return render(request, "about_detail.html")


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

 
# LIST
def project_list(request):
    projects = Project.objects.all()
    return render(request, "projects/project_list.html", {"projects": projects})


# DETAIL
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "projects/project_detail.html", {"project": project})


# CREATE
@login_required()
def create_project(request):
    if request.method == "POST":
        project = Project.objects.create(
            title=request.POST.get("title"),
            client_name=request.POST.get("client_name"),
            short_description=request.POST.get("short_description"),
            description=request.POST.get("description"),
            technologies=request.POST.get("technologies"),
            image=request.FILES.get("image"),
            live_url=request.POST.get("live_url"),
        )
        messages.success(request, "Project created successfully")
        return redirect("project_list")

    return render(request, "projects/create_project.html")


# UPDATE
@login_required()
def update_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        project.title = request.POST.get("title")
        project.client_name = request.POST.get("client_name")
        project.short_description = request.POST.get("short_description")
        project.description = request.POST.get("description")
        project.technologies = request.POST.get("technologies")
        project.live_url = request.POST.get("live_url")

        if request.FILES.get("image"):
            project.image = request.FILES.get("image")

        project.save()
        messages.success(request, "Project updated successfully")
        return redirect(project.get_absolute_url())

    return render(request, "projects/update_project.html", {"project": project})


# DELETE
@login_required()
def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted")
        return redirect("project_list")

    return render(request, "projects/delete_project.html", {"project": project})


# List all testimonials (for homepage)
def testimonial_list_view(request):
    testimonials = Testimonial.objects.all().order_by("-created_at")
    return render(request, "testimonials/testimonial_list.html", {"testimonials": testimonials})

# Create testimonial
@login_required()
def testimonial_create_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        position = request.POST.get("position")
        company = request.POST.get("company")
        message = request.POST.get("message")
        image = request.FILES.get("image")

        Testimonial.objects.create(
            name=name,
            position=position,
            company=company,
            message=message,
            image=image
        )
        messages.success(request, "Testimonial created successfully.")
        return redirect("testimonial_list")

    return render(request, "testimonials/testimonial_create.html")

# Update testimonial
@login_required()
def testimonial_update_view(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)

    if request.method == "POST":
        testimonial.name = request.POST.get("name")
        testimonial.position = request.POST.get("position")
        testimonial.company = request.POST.get("company")
        testimonial.message = request.POST.get("message")
        if request.FILES.get("image"):
            testimonial.image = request.FILES.get("image")
        testimonial.save()
        messages.success(request, "Testimonial updated successfully.")
        return redirect("testimonial_list")

    return render(request, "testimonials/testimonial_update.html", {"testimonial": testimonial})

# Delete testimonial
@login_required()
def testimonial_delete_view(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully.")
        return redirect("testimonial_list")

    return render(request, "testimonials/testimonial_delete.html", {"testimonial": testimonial})



###### part of Simnawa Music codes ##############

 ## simnawa submit music

def submit_music(request):

    if request.method == "POST":

        artist_name = request.POST.get("artist_name")
        stage_name = request.POST.get("stage_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        location = request.POST.get("location")

        song_title = request.POST.get("song_title")
        genre = request.POST.get("genre")

        featuring_artists = request.POST.get(
            "featuring_artists"
        )

        producer_name = request.POST.get(
            "producer_name"
        )

        artist_bio = request.POST.get(
            "artist_bio"
        )

        song_description = request.POST.get(
            "song_description"
        )

        instagram = request.POST.get(
            "instagram"
        )

        tiktok = request.POST.get(
            "tiktok"
        )

        youtube = request.POST.get(
            "youtube"
        )

        cover_art = request.FILES.get(
            "cover_art"
        )

        audio_file = request.FILES.get(
            "audio_file"
        )

        message = f"""
Artist Name: {artist_name}
Stage Name: {stage_name}

Email: {email}
Phone: {phone}

Location: {location}

Song Title: {song_title}
Genre: {genre}

Featuring Artists: {featuring_artists}
Producer Name: {producer_name}

Artist Bio:
{artist_bio}

Song Description:
{song_description}

Instagram:
{instagram}

TikTok:
{tiktok}

YouTube:
{youtube}
"""

        email_message = EmailMessage(
            subject=f"New Music Submission - {song_title}",
            body=message,
            from_email=email,
            to=["your@email.com"]
        )

        if cover_art:
            email_message.attach(
                cover_art.name,
                cover_art.read(),
                cover_art.content_type
            )

        if audio_file:
            email_message.attach(
                audio_file.name,
                audio_file.read(),
                audio_file.content_type
            )

        email_message.send()

        return redirect(
            "submission_success"
        )

    return render(
        request,
        "submit_music.html"
    )