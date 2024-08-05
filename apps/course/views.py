from django.shortcuts import render, get_object_or_404
from apps.course.models import Course, Enrollment


def quran(request):
    courses = Course.objects.filter(category="Quran")

    return render(request, "quran-course.html", {"courses": courses})


def arabic(request):
    courses = Course.objects.filter(category="Arabic")

    return render(request, "arabic-course.html", {"courses": courses})


def islamic(request):
    courses = Course.objects.filter(category="Islamic")

    return render(request, "islamic-course.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    related = Course.objects.all().exclude(id=id)[:6]

    return render(
        request,
        "course-detail.html",
        {
            "course": course,
            "related": related,
        },
    )
