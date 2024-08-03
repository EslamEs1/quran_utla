from django.shortcuts import render
from apps.about.models import About, How_it_works, Terms, WhyUs, Testimonials


# Create your views here.
def about(request):
    about_content = About.objects.first()
    whyus_content = WhyUs.objects.all()

    return render(
        request,
        "about.html",
        {
            "about_content": about_content,
            "whyus_content": whyus_content,
        },
    )


def terms(request):
    terms_content = Terms.objects.first()
    return render(request, "terms.html", {"terms_content": terms_content})


def how_it_works(request):
    how_content = How_it_works.objects.first()
    return render(request, "how-it-works.html", {"terms_content": how_content})
