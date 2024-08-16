from django.contrib import admin
from apps.dashboard.models import CustomUser, Manager, Student, Families, Instructor, Classes, Tax, BillingMonths, Instructor_Student
# Register your models here.


@admin.register(BillingMonths)
class BillingMonthsAdmin(admin.ModelAdmin):
    pass


@admin.register(Instructor_Student)
class Instructor_StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Families)
class FamiliesAdmin(admin.ModelAdmin):
    pass


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    pass


@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    pass


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    pass
