from django.shortcuts import render
from apps.learning.models import Curriculum, Methodology, Steps_Methodology


def curriculum(request):
    curriculums = Curriculum.objects.first()

    return render(request, "curriculum.html", {"curriculums": curriculums})


def methodology(request):
    methodology = Methodology.objects.first()
    steps = Steps_Methodology.objects.all()

    return render(
        request, "curriculum.html", {"steps": steps, "methodology": methodology}
    )


def testimonial(request):
    return render(request, "curriculum.html", {})
