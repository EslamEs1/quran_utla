from django.urls import path
from apps.about import views


app_name = "about"

urlpatterns = [
    path("", views.about, name="about"),
    path("terms/", views.terms, name="terms"),
    path("how-it-works/", views.how_it_works, name="how_it_works"),
]
