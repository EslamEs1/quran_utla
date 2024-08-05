from django.contrib import admin
from .models import (
    Curriculum,
    Methodology,
    Steps_Methodology,
    Steps_To_Start,
    Study_Plan,
)


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ("description",)
    search_fields = ("description",)


@admin.register(Methodology)
class MethodologyAdmin(admin.ModelAdmin):
    list_display = ("description",)
    search_fields = ("description",)


@admin.register(Steps_Methodology)
class StepsMethodologyAdmin(admin.ModelAdmin):
    list_display = ("name", "img", "content")
    search_fields = ("name", "content")


@admin.register(Steps_To_Start)
class StepsToStartAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Study_Plan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
