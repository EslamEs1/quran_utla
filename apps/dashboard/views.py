from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomAuthenticationForm
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count
from .forms import (
    BaseUserForm,
    InstructorForm,
    FamiliesForm,
    StudentForm,
    Instructor_StudentForm,
    ClassesForm,
    BootstrapPasswordChangeForm,
    AdminPasswordChangeForm,
    DiscountsForm,
)
from .models import (
    UserType,
    Tax,
    Instructor_Student,
    Student,
    CustomUser,
    Instructor,
    Families,
    Classes,
    Discounts,
)


@login_required
def dash(request):
    return render(request, "dashboard/dashboard.html")


@login_required
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


@login_required
def billing_month(request):
    return render(request, "dashboard/billingmonths.html")


@login_required
def register_manager(request):
    managers = CustomUser.objects.filter(type=UserType.MANAGER)
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
        "managers": managers,
    }
    return render(request, "dashboard/manager.html", context)


@login_required
def register_instructor(request):
    instructor = Instructor.objects.all()
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
        instructor_form = InstructorForm()

    context = {
        "base_form": base_form,
        "instructor_form": instructor_form,
        "instructor": instructor,
    }
    return render(request, "dashboard/instructor.html", context)


@login_required
def register_family(request):
    families = Families.objects.all()
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
        "families": families,
    }
    return render(request, "dashboard/families.html", context)


@login_required
def register_student(request):
    students = Student.objects.all()
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
        "students": students,
        "student_form": student_form,
    }
    return render(request, "dashboard/student.html", context)


@login_required
def instructor_student_view(request):
    inst_student = Instructor_Student.objects.all()
    if request.method == "POST":
        form = Instructor_StudentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "تم اضافة طالب لمعلم بنجاح")
            return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "لم يتم إضافة طالب لمعلم")
    else:
        form = Instructor_StudentForm()

    context = {
        "form": form,
        "inst_student": inst_student,
    }
    return render(request, "dashboard/instructor_student.html", context)


@login_required
def change_password(request):
    admin_change = AdminPasswordChangeForm()
    if request.method == "POST":
        form = BootstrapPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session
            messages.success(request, "تم تغيير كلمة المرور بنجاح!")
            return redirect(
                "profile"
            )  # Replace 'profile' with your desired redirect URL after password change
        else:
            messages.error(request, "يرجى تصحيح الأخطاء الموجودة في النموذج.")
    else:
        form = BootstrapPasswordChangeForm(request.user)
    return render(
        request,
        "dashboard/change_password.html",
        {"form": form, "admin_change": admin_change},
    )


def admin_password_change(request):
    if request.method == "POST":
        form = AdminPasswordChangeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تغيير كلمة المرور بنجاح!")
            return redirect(
                "dash:dashboard"
            )  # Redirect to a desired view after successful password change
        else:
            messages.error(request, "يرجى تصحيح الأخطاء الموجودة في النموذج.")
            return redirect("dash:dashboard")
    return redirect("dash:dashboard")


def user_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            phone = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(
                request, username=phone, password=password
            )  # use username to pass phone
            if user is not None:
                login(request, user)
                messages.success(request, "تم تسجيل الدخول بنجاح!")
                return redirect("dash:dashboard")
            else:
                messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
        else:
            messages.error(request, "يرجى تصحيح الأخطاء الموجودة في النموذج.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "dashboard/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("dash:dashboard")


def get_students_by_family(request, family_id):
    students = Student.objects.filter(family_id=family_id).values("id", "user__name")
    return JsonResponse({"students": list(students)})


@login_required
def classes(request):
    classes_list = Classes.objects.all()
    if request.method == "POST":
        form = ClassesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "تم اضافة الحصة بنجاح")
                return HttpResponseRedirect(request.headers.get("referer"))
            except Instructor_Student.DoesNotExist:
                messages.error(request, "لا يوجد معلم مرتبط بهذا الطالب")
        else:
            messages.error(
                request, "ربما هناك حقول فارغة او لا يوجد معلم مرتبط بهذا الطالب"
            )
    else:
        form = ClassesForm()

    context = {
        "form": form,
        "classes": classes_list,
    }
    return render(request, "dashboard/classes.html", context)


def invoices(request):
    families = Families.objects.all()

    # Default to current month if not specified in GET parameters
    current_date = datetime.now()
    start_date = current_date.replace(day=1).date()  # First day of the current month
    end_date = start_date.replace(day=1, month=start_date.month + 1) - timedelta(
        days=1
    )  # Last day of the current month

    # Handle form submission for month filter
    if request.method == "GET" and "filter_month" in request.GET:
        selected_month = request.GET.get("filter_month")
        year, month = selected_month.split("-")
        start_date = datetime(
            int(year), int(month), 1
        ).date()  # First day of selected month
        end_date = start_date.replace(day=1, month=int(month) + 1) - timedelta(
            days=1
        )  # Last day of selected month

    # Query invoices for the selected month
    invoices = Classes.objects.filter(date__range=[start_date, end_date])

    # Calculate overall totals for the selected month
    overall_totals = Classes.get_overall_totals(start_date, end_date)

    # Calculate family totals for the selected month
    family_totals = {
        str(family.id): Classes.get_family_totals(family, start_date, end_date)
        for family in families
    }

    return render(
        request,
        "dashboard/family_invoices.html",
        {
            "families": families,
            "family_totals": family_totals,
            "current_date": current_date,
            "overall_totals": overall_totals,
            "invoices": invoices,
        },
    )


def family_invoice_details(request, family_id):
    family = get_object_or_404(Families, pk=family_id)
    students = Student.objects.filter(family=family)

    # Get the latest tax percentage
    latest_tax = Tax.objects.latest("date")
    tax_percentage = latest_tax.percentage if latest_tax else 0.0

    for student in students:
        # Calculate totals for each student
        classes = Classes.objects.filter(student=student)
        total_hours = (
            classes.aggregate(total_hours=Sum("number_class_hours"))["total_hours"] or 0
        )
        total_classes = (
            classes.aggregate(total_classes=Count("id"))["total_classes"] or 0
        )

        total_before_tax = total_hours * student.hourly_salary
        total_after_tax = total_before_tax * (1 - tax_percentage / 100)

        # Assign totals to student objects
        student.total_hours = total_hours
        student.total_classes = total_classes
        student.total_before_tax = total_before_tax
        student.total_after_tax = total_after_tax

    return render(
        request,
        "dashboard/family_invoice_detail.html",
        {
            "family": family,
            "students": students,
            "tax_percentage": tax_percentage,
        },
    )


def student_invoice_details(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    classes = Classes.objects.filter(student=student)

    # Get the latest tax percentage
    latest_tax = Tax.objects.latest("date")
    tax_percentage = latest_tax.percentage if latest_tax else 0.0

    # Calculate totals for the student
    total_hours = (
        classes.aggregate(total_hours=Sum("number_class_hours"))["total_hours"] or 0
    )
    total_classes = classes.count()
    total_before_tax = total_hours * student.hourly_salary
    total_after_tax = total_before_tax * (1 - tax_percentage / 100)

    return render(
        request,
        "dashboard/student_invoice_detail.html",
        {
            "student": student,
            "classes": classes,
            "total_hours": total_hours,
            "total_classes": total_classes,
            "total_before_tax": total_before_tax,
            "total_after_tax": total_after_tax,
            "tax_percentage": tax_percentage,
        },
    )


def instructor_invoices(request):
    instructors = Instructor.objects.all()

    # Default to current month if not specified in GET parameters
    current_date = datetime.now()
    start_date = current_date.replace(day=1).date()  # First day of the current month
    end_date = start_date.replace(day=1, month=start_date.month + 1) - timedelta(
        days=1
    )  # Last day of the current month

    # Handle form submission for month filter
    if request.method == "GET" and "filter_month" in request.GET:
        selected_month = request.GET.get("filter_month")
        year, month = selected_month.split("-")
        start_date = datetime(
            int(year), int(month), 1
        ).date()  # First day of selected month
        end_date = start_date.replace(day=1, month=int(month) + 1) - timedelta(
            days=1
        )  # Last day of selected month

    # Query invoices for the selected month
    invoices = Classes.objects.filter(date__range=[start_date, end_date])

    # Calculate overall totals for the selected month
    overall_totals = Classes.get_overall_totals(start_date, end_date)

    # Calculate instructor totals for the selected month
    instructor_totals = {
        instructor.id: Classes.get_instructor_totals(instructor, start_date, end_date)
        for instructor in instructors
    }

    return render(
        request,
        "dashboard/instructor_invoices.html",
        {
            "instructors": instructors,
            "instructor_totals": instructor_totals,
            "current_date": current_date,
            "overall_totals": overall_totals,
            "invoices": invoices,
        },
    )


def advancesdisc(request):
    disc = Discounts.objects.all()
    if request.method == "POST":
        form = DiscountsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تسجيل السلفه بنجاح!")
            return redirect("dash:advancesdisc")   
        else:
            messages.error(request, "لم يتم تسجيل السلفة")
    else:
        form = DiscountsForm()
    return render(request, "dashboard/advancesdisc.html", {"form": form, "disc":disc,})


def invoices_link(request):
    families = Families.objects.all()
    return render(request, "dashboard/invoices_link.html", {"families": families})



