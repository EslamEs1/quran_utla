from django.urls import path
from apps.blog import views


app_name = "blog"

urlpatterns = [
    path("", views.blog, name="blog"),
    path("<str:slug>/", views.blog_detail, name="blog_detail"),
]
