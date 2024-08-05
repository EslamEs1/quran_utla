from django.contrib import admin
from .models import About, WhyUs, Testimonials, How_it_works, Terms
from django_summernote.admin import SummernoteModelAdmin


class SomeModelAdmin(SummernoteModelAdmin):
    summernote_fields = "__all__"


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("content", "url")
    search_fields = ("content",)


@admin.register(WhyUs)
class WhyUsAdmin(admin.ModelAdmin):
    list_display = ("name", "img", "content")
    search_fields = ("name",)


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "content")
    search_fields = ("name", "position")


@admin.register(How_it_works)
class HowItWorksAdmin(admin.ModelAdmin):
    list_display = ("content",)
    search_fields = ("content",)


@admin.register(Terms)
class TermsAdmin(SomeModelAdmin, admin.ModelAdmin):
    list_display = ("content",)
    search_fields = ("content",)
