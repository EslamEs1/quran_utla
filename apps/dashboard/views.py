from django.shortcuts import render
from apps.dashboard.models import Tax
from django.contrib import messages
from django.http import HttpResponseRedirect


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
