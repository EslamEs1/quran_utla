from django.urls import path
from apps.main import views


app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("teacher/", views.teacher, name="teacher"),
    path("pricing/", views.pricing, name="pricing"),
    path("order/", views.order, name="order"),
]
