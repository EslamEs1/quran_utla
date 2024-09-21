from apps.about.models import Testimonials
from apps.learning.models import Steps_To_Start, Study_Plan
from apps.main.models import Settings
from apps.about.models import About, WhyUs, QuestionAnswer, TestimonialsVideo


def context(request):
    return {
        "testimonials": Testimonials.objects.all(),
        "steps_to_start": Steps_To_Start.objects.all(),
        "study_plan": Study_Plan.objects.all(),
        "settings": Settings.objects.first(),  # Assuming there's only one settings object in the database.
        "about": About.objects.first(),
        "testimonials_video": TestimonialsVideo.objects.first(),
        "questionanswer": QuestionAnswer.objects.first(),
        "whyus": WhyUs.objects.all(),  # Assuming there's only one whyus object in the database.
    }
