from django.urls import path
from apps.learning import views


app_name = "course"

urlpatterns = [
    path("curriculum/", views.curriculum, name="curriculum"),
    path("testimonials/", views.testimonial, name="testimonials"),
    path("teaching-methodology/", views.methodology, name="methodology"),
]
