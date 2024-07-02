from django.urls import path
from apps.dashboard import views


app_name = "dash"

urlpatterns = [
    path("", views.dash, name="dashboard"),
    path("tax/", views.tax, name="tax"),
    path("billing-month/", views.billing_month, name="billing_month"),
    path("register-user/", views.register_user, name="register_user"),
]
