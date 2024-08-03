from apps.about.models import Testimonials
from apps.learning.models import Steps_To_Start, Study_Plan
from apps.main.models import Settings


def context(request):
    return {
        "testimonials": Testimonials.objects.all(),
        "steps_to_start": Steps_To_Start.objects.all(),
        "study_plan": Study_Plan.objects.all(),
        "settings": Settings.objects.first(),  # Assuming there's only one settings object in the database.
    }
