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


def register_user(request):
    if request.method == "POST":
        base_form = BaseUserForm(request.POST)
        user_type = request.POST.get("manager")
        if user_type:
            if user_type == UserType.MANAGER:
                if base_form.is_valid():
                    base_form.save()
                    messages.success(request, f"تم اضافة مشرف جديد بنجاح")
                    return HttpResponseRedirect(request.headers.get("referer"))
                else:
                    messages.error(request, "لم يتم الحفظ")
    else:
        base_form = BaseUserForm()

    context = {"base_form": base_form}
    return render(request, "dashboard/register_user.html", context)


