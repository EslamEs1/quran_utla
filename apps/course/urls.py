from django.urls import path
from apps.course import views


app_name = "course"

urlpatterns = [
    path("quran/", views.quran, name="quran"),
    path("arabic/", views.arabic, name="arabic"),
    path("islamic/", views.islamic, name="islamic"),
    path("detail/<str:slug>/", views.course_detail, name="course_detail"),
]
