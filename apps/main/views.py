from django.shortcuts import render
from apps.main.models import (
    ContactUs,
    Pricing,
    Fees,
    Pricing_Content,
    TeacherContact,
    Slider,
    Tutors,
)
from django.contrib.auth import get_user_model
from apps.course.models import Course
from apps.blog.models import Post
from django.contrib import messages
from django.http import HttpResponseRedirect
from apps.dashboard.models import UserType, Student, Families

User = get_user_model()


def index(request):
    sliders = Slider.objects.all()
    courses = Course.objects.all()
    try:
        student = Student.objects.filter(is_active=True).count()
        family = Families.objects.filter(is_active=True).count()
        teacher = User.objects.filter(type=UserType.INSTRUCTOR, is_active=True).count()
        
    except:
        student = 0
        family = 0
        teacher = 0
    tutors = Tutors.objects.all()
    posts = Post.objects.all()

    return render(
        request,
        "index.html",
        {
            "sliders": sliders,
            "courses": courses,
            "student": student,
            "family": family,
            "teacher": teacher,
            "tutors": tutors,
            "posts": posts,
        },
    )


def pricing(request):
    pricing_content = Pricing_Content.objects.first()
    pricing = Pricing.objects.all()
    fees = Fees.objects.all()

    return render(
        request,
        "pricing.html",
        {"pricing_content": pricing_content, "pricing": pricing, "fees": fees},
    )


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        whatsapp = request.POST.get("whatsapp")
        message = request.POST.get("message")

        ContactUs.objects.create(
            name=name, email=email, whatsapp=whatsapp, message=message
        )
        messages.success(request, "The Message Have Been Sent")
        return HttpResponseRedirect(request.headers.get("referer"))

    return render(request, "contact.html", {})


def teacher(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        subject = request.POST.get("subject")
        qualifications = request.POST.get("qualifications")
        message = request.POST.get("message")

        TeacherContact.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            subject=subject,
            qualifications=qualifications,
            message=message,
        )
        messages.success(request, "The Message Have Been Sent")
        return HttpResponseRedirect(request.headers.get("referer"))

    return render(request, "teacher.html", {})
