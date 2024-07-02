from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import BaseUserForm, ManagerForm, InstructorForm, FamiliesForm, StudentForm
from .models import (
    UserType,
    Tax,
    Manager,
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


def register_user(request):
    if request.method == "POST":
        user_type = request.POST.get("type")
        base_form = BaseUserForm(request.POST)

        if user_type == UserType.MANAGER:
            form = ManagerForm(request.POST)
        elif user_type == UserType.INSTRUCTOR:
            form = InstructorForm(request.POST)
        elif user_type == UserType.FAMILIES:
            form = FamiliesForm(request.POST)
        elif user_type == UserType.STUDENT:
            form = StudentForm(request.POST)
        else:
            form = BaseUserForm(request.POST)

        if base_form.is_valid() and form.is_valid():
            user = base_form.save(commit=False)
            user.type = user_type
            user.save()

            if user_type == UserType.MANAGER:
                manager = Manager.objects.create(user=user)
            elif user_type == UserType.INSTRUCTOR:
                instructor = form.save(commit=False)
                instructor.user = user
                instructor.save()
            elif user_type == UserType.FAMILIES:
                families = form.save(commit=False)
                families.user = user
                families.save()
            elif user_type == UserType.STUDENT:
                student = form.save(commit=False)
                student.user = user
                student.save()

            return redirect("dashboard")  # Redirect to a success page
    else:
        base_form = BaseUserForm()
        user_type = request.GET.get("type", UserType.STUDENT)
        if user_type == UserType.MANAGER:
            form = ManagerForm()
        elif user_type == UserType.INSTRUCTOR:
            form = InstructorForm()
        elif user_type == UserType.FAMILIES:
            form = FamiliesForm()
        elif user_type == UserType.STUDENT:
            form = StudentForm()
        else:
            form = BaseUserForm()

    context = {"base_form": base_form, "form": form, "user_type": user_type}
    return render(request, "dashboard/register_user.html", context)
