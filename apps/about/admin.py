from django.contrib import admin
from .models import (
    About,
    WhyUs,
    Testimonials,
    How_it_works,
    Terms,
    TestimonialsVideo,
    QuestionAnswer,
)
from django_summernote.admin import SummernoteModelAdmin


class SomeModelAdmin(SummernoteModelAdmin):
    summernote_fields = "__all__"


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("content", "url")
    search_fields = ("content",)

    def has_add_permission(self, request):
        return False if About.objects.count() >= 1 else True


@admin.register(WhyUs)
class WhyUsAdmin(admin.ModelAdmin):
    list_display = ("name", "img", "content")
    search_fields = ("name",)

    def has_add_permission(self, request):
        return False if WhyUs.objects.count() >= 6 else True


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "content")
    search_fields = ("name", "position")


@admin.register(How_it_works)
class HowItWorksAdmin(admin.ModelAdmin):
    list_display = ("content",)
    search_fields = ("content",)

    def has_add_permission(self, request):
        return False if How_it_works.objects.count() >= 1 else True


@admin.register(Terms)
class TermsAdmin(SomeModelAdmin, admin.ModelAdmin):

    def has_add_permission(self, request):
        return False if Terms.objects.count() >= 1 else True


@admin.register(TestimonialsVideo)
class TestimonialsVideoAdmin(SomeModelAdmin, admin.ModelAdmin):

    def has_add_permission(self, request):
        return False if TestimonialsVideo.objects.count() >= 1 else True


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(SomeModelAdmin, admin.ModelAdmin):

    def has_add_permission(self, request):
        return False if QuestionAnswer.objects.count() >= 6 else True
