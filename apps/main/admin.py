from django.contrib import admin
from .models import (
    Slider,
    Settings,
    Pricing_Content,
    Pricing,
    Fees,
    ContactUs,
    TeacherContact,
    Tutors,
)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "img", "content")
    search_fields = ("title", "content")


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "facebook",
        "instagram",
        "twitter",
        "youtube",
        "phone",
        "whatsapp",
        "address",
        "email",
        "map_link",
    )
    search_fields = ("title", "address", "email")

    def has_add_permission(self, request):
        return False if Settings.objects.count() >= 1 else True


@admin.register(Pricing_Content)
class PricingContentAdmin(admin.ModelAdmin):
    list_display = ("content",)
    search_fields = ("content",)


@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ("char", "week", "price", "classes", "hours")
    search_fields = ("char", "week")


@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "whatsapp", "message")
    search_fields = ("name", "email", "message")


@admin.register(TeacherContact)
class TeacherContactAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone_number",
        "subject",
        "created_at",
    )
    search_fields = ("full_name", "email", "phone_number", "subject")
    readonly_fields = ("created_at",)


@admin.register(Tutors)
class TutorsAdmin(admin.ModelAdmin):
    list_display = ("full_name", "image", "qualifications")
    search_fields = ("full_name", "qualifications")
