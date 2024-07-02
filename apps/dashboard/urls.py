from django.urls import path
from apps.dashboard import views


app_name = "dash"

urlpatterns = [
    path("", views.dash, name="dashboard"),
    path("tax/", views.tax, name="tax"),
    path("billing-month/", views.billing_month, name="billing_month"),
    path("register_manager/", views.register_manager, name="register_manager"),
    path("register_instructor/", views.register_instructor, name="register_instructor"),
    path("register_family/", views.register_family, name="register_family"),
    path("register_student/", views.register_student, name="register_student"),
]
