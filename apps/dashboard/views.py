from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import BaseUserForm, InstructorForm, FamiliesForm, StudentForm
from .models import (
    UserType,
    Tax,
)


def dash(request):
    return render(request, "dashboard/dashboard.html")


def tax(request):
    if request.method == "POST":
        tax_number = request.POST.get("tax")
        if tax_number:
            Tax.objects.create(number=tax_number)
            messages.success(request, f"تم اضافة ضريبة % {tax_number} بنجاح")
        else:
            messages.error(request, "لم يتم الحفظ")
        return HttpResponseRedirect(request.headers.get("referer"))

    return render(request, "dashboard/tax.html")


def billing_month(request):
    return render(request, "dashboard/billingmonths.html")


def register_manager(request):
    if request.method == "POST":
        base_form = BaseUserForm(request.POST)
        user_type = request.POST.get("user_type")
        if user_type and user_type == UserType.MANAGER:
            if base_form.is_valid():
                user = base_form.save(commit=False)
                user.type = UserType.MANAGER
                user.save()
                messages.success(request, "تم اضافة مشرف جديد بنجاح")
                return HttpResponseRedirect(request.headers.get("referer"))
            else:
                messages.error(request, "لم يتم الحفظ ربما رقم موجود من قبل")
    else:
        base_form = BaseUserForm()
        
    context = {
        "base_form": base_form,
    }
    return render(request, "dashboard/manager.html", context)


def register_instructor(request):
    if request.method == "POST":
        base_form = BaseUserForm(request.POST)
        instructor_form = InstructorForm(request.POST)
        user_type = request.POST.get("user_type")

        if (
            base_form.is_valid()
            and instructor_form.is_valid()
            and user_type == UserType.INSTRUCTOR
        ):
            user = base_form.save(commit=False)
            user.type = UserType.INSTRUCTOR
            user.save()
            instructor = instructor_form.save(commit=False)
            instructor.user = user
            instructor.save()
            messages.success(request, "تم اضافة معلم جديد بنجاح")
            return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "لم يتم الحفظ ربما رقم موجود من قبل")

    else:
        base_form = BaseUserForm()
        instructor_form = FamiliesForm()

    context = {
        "base_form": base_form,
        "instructor_form": instructor_form,
    }
    return render(request, "dashboard/instructor.html", context)


def register_family(request):
    if request.method == "POST":
        base_form = BaseUserForm(request.POST)
        families_form = FamiliesForm(request.POST)
        user_type = request.POST.get("user_type")

        if (
            base_form.is_valid()
            and families_form.is_valid()
            and user_type == UserType.FAMILIES
        ):
            user = base_form.save(commit=False)
            user.type = UserType.FAMILIES
            user.save()
            family = families_form.save(commit=False)
            family.user = user
            family.save()
            messages.success(request, "تم اضافة عائلة جديدة بنجاح")
            return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "لم يتم الحفظ ربما رقم موجود من قبل")
    else:
        base_form = BaseUserForm()
        families_form = FamiliesForm()

    context = {
        "base_form": base_form,
        "families_form": families_form,
    }
    return render(request, "dashboard/families.html", context)


def register_student(request):
    if request.method == "POST":
        base_form = BaseUserForm(request.POST)
        student_form = StudentForm(request.POST)
        user_type = request.POST.get("user_type")

        if (
            base_form.is_valid()
            and student_form.is_valid()
            and user_type == UserType.STUDENT
        ):
            user = base_form.save(commit=False)
            user.type = UserType.STUDENT
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, "تم اضافة طالب جديد بنجاح")
            return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "لم يتم الحفظ ربما رقم موجود من قبل")
    else:
        base_form = BaseUserForm()
        student_form = StudentForm()

    context = {
        "base_form": base_form,
        "student_form": student_form,
    }
    return render(request, "dashboard/student.html", context)
