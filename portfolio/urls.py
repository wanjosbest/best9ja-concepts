from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services_list, name="services_list"),
    path("services/create/", views.create_service, name="create_service"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("services/<slug:slug>/update/", views.update_service, name="update_service"),
    path("services/<slug:slug>/delete/", views.delete_service, name="delete_service"),
    path("worki/", views.work, name="work"),
    path("blog/", views.blog, name="blog"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("newsletter/subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
    path("blogi/", views.blog_post_list_view, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_post_details_view, name="blog_details"),
    path("blogi/create/", views.create_blog_post_view, name="create_blog_post"),
    path("blog/<slug:slug>/update/", views.update_blog_post_view, name="update_blog_post"),
    path("blog/<slug:slug>/delete/", views.delete_blog_post_view, name="delete_blog_post"),
    path("work/", views.project_list, name="project_list"),
    path("work/create/", views.create_project, name="create_project"),
    path("work/<slug:slug>/", views.project_detail, name="project_detail"),
    path("work/<slug:slug>/update/", views.update_project, name="update_project"),
    path("work/<slug:slug>/delete/", views.delete_project, name="delete_project"),

    path("testimonials/", views.testimonial_list_view, name="testimonial_list"),
    path("testimonials/create/", views.testimonial_create_view, name="testimonial_create"),
    path("testimonials/update/<int:pk>/", views.testimonial_update_view, name="testimonial_update"),
    path("testimonials/delete/<int:pk>/", views.testimonial_delete_view, name="testimonial_delete"),
]
