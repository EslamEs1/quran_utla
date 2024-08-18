from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from .forms import CustomAuthenticationForm
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum, Q
from urllib.parse import quote
from django.db.models import IntegerField
from django.db.models.functions import Cast

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
    Marketer_StudentForm,
    MarketerForm,
)
from decimal import Decimal
from apps.main.models import ContactUs, TeacherContact
from .models import (
    UserType,
    Tax,
    Instructor_Student,
    Student,
    Instructor,
    Families,
    Classes,
    Discounts,
    BillingMonths,
    Manager,
    Marketer_Student,
    Marketer,
    Instructor,
)

CustomUser = get_user_model()


@login_required
def dash(request):
    return render(request, "dashboard/dashboard.html")


# ------------------------------------------------ Billing
@login_required
def tax(request):
    if request.method == "POST":
        tax_number = request.POST.get("tax")
        if tax_number:
            Tax.objects.create(percentage=tax_number)
            messages.success(request, f"تم اضافة ضريبة % {tax_number} بنجاح")
        else:
            messages.error(request, "لم يتم الحفظ")
        return HttpResponseRedirect(request.headers.get("referer"))

    return render(request, "dashboard/tax.html")


@login_required
def billing_month(request):
    billing = BillingMonths.objects.filter()
    family = Families.objects.all()

    if request.method == "POST":
        date = request.POST.get("date")
        fam_id = request.POST.get("family")

        # Convert date string to datetime object
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()

        # Check if a billing entry already exists for the selected date and family
        existing_billing = billing.filter(date=selected_date, family_id=fam_id).exists()

        if not existing_billing:
            try:
                family_obj = Families.objects.get(id=fam_id)
                BillingMonths.objects.create(
                    date=selected_date,
                    family=family_obj,
                )
                messages.success(request, "تم اضافة فترة الفوترة بنجاح")
            except Families.DoesNotExist:
                messages.error(request, "العائلة غير موجودة")
            except Exception as e:
                messages.error(request, f"حدث خطأ: {str(e)}")
        else:
            messages.error(request, "هذا الشهر والعائلة موجودان مسبقاً")

    return render(
        request, "dashboard/billingmonths.html", {"billing": billing, "family": family}
    )


@login_required
def edit_billing_month(request):
    if request.method == "POST":
        date = request.POST.get("date")
        fam = request.POST.get("family")
        if date and fam:
            BillingMonths.objects.filter(family=Families.objects.get(id=fam)).update(
                date=datetime.strptime(date, "%Y-%m-%d"),
            )
            messages.success(request, "تم تعديل فترة الفوترة بنجاح")
        else:
            messages.error(request, "يرجى اختيار تاريخ وعائله")

    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def delete_billing_month(request, id):
    BillingMonths.objects.get(id=id).delete()
    messages.success(request, "تم حذف فترة الفوترة بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


# ------------------------------------------------ Manager
@login_required
def register_manager(request):
    search_query = request.GET.get("search", "")
    if search_query:
        managers = CustomUser.objects.filter(
            (
                Q(name__icontains=search_query)
                | Q(phone__icontains=search_query)
                | Q(address__icontains=search_query)
            )
            & Q(is_active=True)
            & Q(type=UserType.MARKETER)
        )
    else:
        managers = CustomUser.objects.filter(type=UserType.MANAGER, is_active=True)

    if request.method == "POST":
        base_form = BaseUserForm(request.POST)
        user_type = request.POST.get("user_type")
        if user_type and user_type == UserType.MANAGER:
            if base_form.is_valid():
                user = base_form.save(commit=False)
                user.type = UserType.MANAGER
                user.set_password(
                    base_form.cleaned_data["password"]
                )  # Ensure password is hashed
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
        "search_query": search_query,
    }
    return render(request, "dashboard/manager.html", context)


@login_required
def edit_manager(request, id):
    manager = get_object_or_404(CustomUser, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        age = request.POST.get("age")

        if name and phone and address and gender and age:
            # Update the manager's details
            manager.name = name
            manager.phone = phone
            manager.address = address
            manager.gender = gender
            manager.age = age
            manager.save()  # Save the changes to the database

            messages.success(request, "تم تعديل المشرف بنجاح")
            return redirect("dash:register_manager")
        else:
            messages.error(request, "حدث خطأ أثناء تعديل المشرف")


@login_required
def delete_manager(request, id):
    manager = get_object_or_404(CustomUser, id=id)
    manager.is_active = False
    manager.save()
    messages.success(request, "تم حذف المشرف بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


# ------------------------------------------------ Instructor
@login_required
def register_instructor(request):
    search_query = request.GET.get("search", "")
    if search_query:
        instructor = Instructor.objects.filter(
            (
                Q(user__name__icontains=search_query)
                | Q(user__phone__icontains=search_query)
                | Q(user__address__icontains=search_query)
            )
            & Q(user__is_active=True)  # Correct placement of the '&' operator
        )
    else:
        instructor = Instructor.objects.filter(user__is_active=True)

    managers = CustomUser.objects.filter(type=UserType.MANAGER, is_active=True)

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
            user.set_password(base_form.cleaned_data["password"])
            if request.user.type == UserType.MANAGER:
                manager_instance = Manager.objects.get(user=request.user)
                instructor.manager = manager_instance
            instructor.save()
            messages.success(request, "تم اضافة معلم جديد بنجاح")
            return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "لم يتم الحفظ ربما رقم موجود من قبل")

    else:
        base_form = BaseUserForm()
        instructor_form = InstructorForm(user=request.user)

    context = {
        "base_form": base_form,
        "instructor_form": instructor_form,
        "instructor": instructor,
        "search_query": search_query,
        "managers": managers,
    }
    return render(request, "dashboard/instructor.html", context)


@login_required
def edit_instructor(request, id):
    custom_user = get_object_or_404(CustomUser, id=id)
    instructor = get_object_or_404(Instructor, user=custom_user)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        manager_id = request.POST.get("manager")
        qualification = request.POST.get("qualification")
        hourly_salary = request.POST.get("hourly_salary")
        class_link = request.POST.get("class_link")
        id_number = request.POST.get("id_number")

        if (
            name
            and phone
            and address
            and gender
            and age
            and manager_id
            and qualification
            and hourly_salary
            and class_link
            and id_number
        ):
            try:
                custom_user.name = name
                custom_user.phone = phone
                custom_user.address = address
                custom_user.gender = gender
                custom_user.age = age
                instructor.manager = Manager.objects.get(user__id=manager_id)
                instructor.qualification = qualification
                instructor.hourly_salary = hourly_salary
                instructor.class_link = class_link
                instructor.id_number = id_number
                custom_user.save()  # Save changes to CustomUser
                instructor.save()  # Save changes to Families

                messages.success(request, "تم تعديل المعلم بنجاح")
            except Manager.DoesNotExist:
                messages.error(request, "المشرف المحدد غير موجود أو ليس مشرفاً.")
        else:
            messages.error(request, "حدث خطأ أثناء تعديل المعلم")

    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def delete_instructor(request, id):
    instructor = get_object_or_404(CustomUser, id=id)
    instructor.is_active = False
    instructor.save()
    messages.success(request, "تم حذف المعلم بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


# ------------------------------------------------ Families
@login_required
def register_family(request):
    search_query = request.GET.get("search", "")
    if search_query:
        families = Families.objects.filter(
            (
                Q(name__icontains=search_query)
                | Q(number__icontains=search_query)
                | Q(address__icontains=search_query)
            )
            & Q(is_active=True)
        )
    else:
        families = Families.objects.filter(is_active=True)

    managers = CustomUser.objects.filter(type=UserType.MANAGER, is_active=True)

    if request.method == "POST":
        families_form = FamiliesForm(request.POST, user=request.user)
        if families_form.is_valid():
            family = families_form.save(commit=False)
            if request.user.type == UserType.MANAGER:
                manager_instance = Manager.objects.get(user=request.user)
                family.manager = manager_instance
            family.save()
            messages.success(request, "تم اضافة عائلة جديدة بنجاح")
            return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "لم يتم الحفظ ربما رقم موجود من قبل")
    else:
        families_form = FamiliesForm(user=request.user)

    context = {
        "families_form": families_form,
        "families": families,
        "managers": managers,
        "search_query": search_query,
    }
    return render(request, "dashboard/families.html", context)


@login_required
def edit_family(request, id):
    family = get_object_or_404(Families, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        manager_id = request.POST.get("manager")
        the_state = request.POST.get("the_state")
        payment_link = request.POST.get("payment_link")

        if (
            name
            and phone
            and address
            and gender
            and manager_id
            and the_state
            and payment_link
        ):
            try:
                family.name = name
                family.number = phone
                family.address = address
                family.gender = gender
                family.manager = Manager.objects.get(user__id=manager_id)
                family.the_state = the_state
                family.payment_link = payment_link
                family.save()  # Save changes to CustomUser

                messages.success(request, "تم تعديل العائلة بنجاح")
            except Manager.DoesNotExist:
                messages.error(request, "المشرف المحدد غير موجود أو ليس مشرفاً.")
        else:
            messages.error(request, "حدث خطأ أثناء تعديل العائلة")

    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def delete_family(request, id):
    family = get_object_or_404(Families, id=id)
    family.is_active = False
    family.save()
    messages.success(request, "تم حذف العائلة بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


# ------------------------------------------------ Student
@login_required
def register_student(request):
    search_query = request.GET.get("search", "")
    if search_query:
        students = Student.objects.filter(name__icontains=search_query, is_active=True)
    else:
        students = Student.objects.filter(is_active=True)

    families = Families.objects.all()
    if request.method == "POST":
        student_form = StudentForm(request.POST)

        if student_form.is_valid():
            student_form.save()
            messages.success(request, "تم اضافة طالب جديد بنجاح")
            return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "لم يتم الحفظ ربما رقم موجود من قبل")
    else:
        student_form = StudentForm()

    context = {
        "families": families,
        "students": students,
        "student_form": student_form,
        "search_query": search_query,
    }
    return render(request, "dashboard/student.html", context)


@login_required
def instructor_student_view(request):
    inst_student = Instructor_Student.objects.all()

    if request.method == "POST":
        form = Instructor_StudentForm(request.POST)

        if form.is_valid():
            # Extract student and instructor from form data
            student_id = form.cleaned_data["student"].id
            instructor_id = form.cleaned_data["instructor"].id

            # Check if relationship already exists
            if inst_student.filter(
                student_id=student_id, instructor_id=instructor_id
            ).exists():
                messages.error(request, "الطالب مرتبط بالفعل بالمعلم.")
            else:
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
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        family_id = request.POST.get("family")
        payment_link = request.POST.get("payment_link")
        hourly_salary = request.POST.get("hourly_salary")

        if name and gender and age and family_id and hourly_salary and payment_link:
            try:
                student.name = name
                student.gender = gender
                student.age = age
                student.family = Families.objects.get(id=family_id)
                student.hourly_salary = hourly_salary
                student.payment_link = payment_link
                student.save()

                messages.success(request, "تم تعديل الطالب بنجاح")
            except Manager.DoesNotExist:
                messages.error(request, "المشرف المحدد غير موجود أو ليس مشرفاً.")
        else:
            messages.error(request, "حدث خطأ أثناء تعديل الطالب")

    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.is_active = False
    student.save()
    messages.success(request, "تم حذف الطالب بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def del_student_instructor(request, id):
    student = get_object_or_404(Instructor_Student, id=id)
    student.delete()
    messages.success(request, "تم حذف الطالب من المعلم بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


# ------------------------------------------------ Password
@login_required
def change_password(request):
    admin_change = AdminPasswordChangeForm()
    if request.method == "POST":
        form = BootstrapPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session
            messages.success(request, "تم تغيير كلمة المرور بنجاح!")
            return redirect("dash:dashboard") 
        else:
            messages.error(request, "يرجى تصحيح الأخطاء الموجودة في النموذج.")
    else:
        form = BootstrapPasswordChangeForm(request.user)
    return render(
        request,
        "dashboard/change_password.html",
        {"form": form, "admin_change": admin_change},
    )


@login_required
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


# ------------------------------------------------ Login
def user_login(request):
    if request.user.is_authenticated:
        return redirect("dash:dashboard")

    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            phone = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=phone, password=password)
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
    return redirect("dash:login")


# ------------------------------------------------ Student By Family
def get_students_by_family(request, family_id):
    user = request.user
    if user.type == UserType.INSTRUCTOR:
        try:
            instructor_instance = Instructor.objects.get(user=user)
            students = Student.objects.filter(
                family_id=family_id,
                id__in=Instructor_Student.objects.filter(
                    instructor=instructor_instance
                ).values_list("student", flat=True),
            ).values("id", "name")
        except Instructor.DoesNotExist:
            students = Student.objects.none()
    else:
        students = Student.objects.filter(family_id=family_id).values("id", "name")

    print("Students:", list(students))  # Debugging line
    return JsonResponse({"students": list(students)})


# ------------------------------------------------ Markter
@login_required
def register_marketer(request):
    search_query = request.GET.get("search", "")
    if search_query:
        marketer = Marketer.objects.filter(
            (
                Q(user__name__icontains=search_query)
                | Q(user__phone__icontains=search_query)
                | Q(user__address__icontains=search_query)
            )
            & Q(user__is_active=True)
            & Q(user__type=UserType.MARKETER)
        )
    else:
        marketer = Marketer.objects.filter(
            user__type=UserType.MARKETER, user__is_active=True
        )

    if request.method == "POST":
        base_form = BaseUserForm(request.POST)
        marketer_form = MarketerForm(request.POST)
        user_type = request.POST.get("user_type")

        if user_type and user_type == UserType.MARKETER:
            if base_form.is_valid() and marketer_form.is_valid():
                user = base_form.save(commit=False)
                user.type = UserType.MARKETER
                user.set_password(base_form.cleaned_data["password"])
                user.save()

                marketer = marketer_form.save(commit=False)
                marketer.user = user
                marketer.save()

                messages.success(request, "تم اضافة مسوق جديد بنجاح")
                return HttpResponseRedirect(request.headers.get("referer"))
            else:
                messages.error(request, "لم يتم الحفظ ربما رقم موجود من قبل")
    else:
        marketer_form = MarketerForm()
        base_form = BaseUserForm()

    context = {
        "base_form": base_form,
        "marketer": marketer,
        "search_query": search_query,
        "marketer_form": marketer_form,
    }
    return render(request, "dashboard/marketer.html", context)


@login_required
def edit_markter(request, id):
    manager = get_object_or_404(CustomUser, id=id)
    marketer = get_object_or_404(Marketer, user=manager)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        ratio = request.POST.get("ratio")
        salary = request.POST.get("salary")

        if name and phone and address and gender and age and ratio and salary:
            # Update the manager's details
            manager.name = name
            marketer.ratio = ratio
            marketer.salary = salary
            manager.phone = phone
            manager.address = address
            manager.gender = gender
            manager.age = age
            manager.save()
            marketer.save()

            messages.success(request, "تم تعديل المسوق بنجاح")
            return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "حدث خطأ أثناء تعديل المسوق")
            return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def delete_markter(request, id):
    manager = get_object_or_404(CustomUser, id=id)
    manager.is_active = False
    manager.save()
    messages.success(request, "تم حذف المشرف بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def marketer_student_view(request):
    mar_student = Marketer_Student.objects.all()

    if request.method == "POST":
        form = Marketer_StudentForm(request.POST)

        if form.is_valid():
            # Extract student and instructor from form data
            student_id = form.cleaned_data["student"].id
            marketer_id = form.cleaned_data["marketer"].id
            # Check if relationship already exists
            if mar_student.filter(
                student_id=student_id, marketer_id=marketer_id
            ).exists():
                messages.error(request, "الطالب مرتبط بالفعل بالمسوق.")
            else:
                form.save()
                messages.success(request, "تم اضافة طالب لمسوق بنجاح")
                return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "لم يتم إضافة طالب مسوق")
    else:
        form = Marketer_StudentForm()

    context = {
        "form": form,
        "mar_student": mar_student,
    }
    return render(request, "dashboard/marketer_student.html", context)


@login_required
def del_student_marketer(request, id):
    student = get_object_or_404(Marketer_Student, id=id)
    student.delete()
    messages.success(request, "تم حذف الطالب من المسوق بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


# ------------------------------------------------ Classes
@login_required
def classes(request):
    # Default to current month if not specified in GET parameters
    current_date = datetime.now()
    start_date = current_date.replace(day=1).date()  # First day of the current month
    end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(
        day=1
    ) - timedelta(
        days=1
    )  # Last day of the current month

    # Handle form submission for month filter
    if request.method == "GET" and "filter_month" in request.GET:
        selected_month = request.GET.get("filter_month")
        year, month = selected_month.split("-")
        start_date = datetime(
            int(year), int(month), 1
        ).date()  # First day of selected month
        end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(
            day=1
        ) - timedelta(
            days=1
        )  # Last day of selected month

    search_query = request.GET.get("search", "")

    if request.user.type == UserType.INSTRUCTOR:
        # Filter classes only for the instructor, including search if provided
        classes_list = Classes.objects.filter(
            instructor__user=request.user, created_at__range=[start_date, end_date]
        )

        if search_query:
            classes_list = classes_list.filter(
                Q(family__name__icontains=search_query)
                | Q(student__name__icontains=search_query)
                | Q(instructor__user__name__icontains=search_query)
            )
    else:
        # For non-instructors, filter classes based on the search query if provided
        classes_list = Classes.objects.filter(created_at__range=[start_date, end_date])

        if search_query:
            classes_list = classes_list.filter(
                Q(family__name__icontains=search_query)
                | Q(student__name__icontains=search_query)
                | Q(instructor__user__name__icontains=search_query)
            )

    if request.method == "POST":
        form = ClassesForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                form_2 = form.save(commit=False)
                if request.user.type == UserType.INSTRUCTOR:
                    instructor_instance = Instructor.objects.get(user=request.user)
                    form_2.instructor = instructor_instance
                form_2.save()
                messages.success(request, "تم اضافة الحصة بنجاح")
                return HttpResponseRedirect(request.headers.get("referer"))
            except Instructor_Student.DoesNotExist:
                messages.error(request, "لا يوجد معلم مرتبط بهذا الطالب")
        else:
            messages.error(
                request, "ربما هناك حقول فارغة او لا يوجد معلم مرتبط بهذا الطالب"
            )
    else:
        form = ClassesForm(user=request.user)

    families = Families.objects.all()
    students = Student.objects.all()
    instructors = Instructor.objects.all()
    
    context = {
        "form": form,
        "classes": classes_list,
        "families": families,
        "students": students,
        "instructors": instructors,
    }
    return render(request, "dashboard/classes.html", context)


@login_required
def edit_classes(request, id):
    classes = get_object_or_404(Classes, id=id)

    if request.method == "POST":
        # family = request.POST.get("family")
        # student = request.POST.get("student")
        date = request.POST.get("date")
        number_class_hours = request.POST.get("number_class_hours")
        evaluation = request.POST.get("evaluation")
        subject_name = request.POST.get("subject_name")
        notes = request.POST.get("notes")

        if date and number_class_hours and evaluation and subject_name and notes:
            classes.date = date
            classes.number_class_hours = number_class_hours
            classes.evaluation = evaluation
            classes.subject_name = subject_name
            classes.notes = notes
            classes.save()
            messages.success(request, "تم تعديل الحصة بنجاح")
        else:
            messages.error(request, "حدث خطأ أثناء تعديل الحصة")

    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def delete_classes(request, id):
    student = get_object_or_404(Classes, id=id)
    student.delete()
    messages.success(request, "تم حذف الحصة بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


# ------------------------------------------------ Invoices
def invoices(request):
    if not request.user.type == "Admin":
        return redirect("dash:dashboard")

    search_query = request.GET.get("search", "")

    families = Families.objects.filter(is_active=True)

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

    families_with_classes = Families.objects.filter(
        is_active=True, student__classes__date__range=[start_date, end_date]
    ).distinct()

    if search_query:
        families_with_classes = families_with_classes.filter(name__icontains=search_query)

    # Query invoices for the selected month
    invoices = Classes.objects.filter(date__range=[start_date, end_date])

    # Calculate overall totals for the selected month
    overall_totals = Classes.get_overall_totals(start_date, end_date)

    total_hours = overall_totals["total_hours"] // 60

    # Calculate family totals for the selected month
    family_totals = {
        str(family.id): Classes.get_family_totals(family, start_date, end_date)
        for family in families_with_classes
    }

    message = (
        "السلام عليكم ورحمة الله وبركاته\n"
        "🌹الإدارة المالية لمركز  قران يتلى تتمنى لكم التوفيق🌹\n"
        f"تم اصدار فاتورة شهر {current_date.strftime('%B %Y')}\n"
        f"إجمالي المستحقات  لهذا الشهر {overall_totals['total_salary']}\n"
        "يمكنكم مراجعة الفاتورة من خلال هذا الرابط\n"
    )
    encoded_message = quote(message)  # URL encode the message

    return render(
        request,
        "dashboard/family_invoices.html",
        {
            "families": families,
            "family_totals": family_totals,
            "current_date": current_date,
            "overall_totals": overall_totals,
            "invoices": invoices,
            "encoded_message": encoded_message,
            "total_hours": total_hours,
        },
    )


def family_invoice_details(request, family_id):
    family = get_object_or_404(Families, pk=family_id, is_active=True)
    students = Student.objects.filter(family=family)

    try:
        billing_month = BillingMonths.objects.get(family=family)
        selected_date = billing_month.date
    except BillingMonths.DoesNotExist:
        selected_date = None

    if not selected_date:
        current_date = datetime.now().date()
        selected_date = current_date.replace(day=1)
    try:
        latest_tax = Tax.objects.latest("date")
    except Tax.DoesNotExist:
        latest_tax = Tax(percentage=0.0)

    tax_percentage = latest_tax.percentage if latest_tax else 0.0

    total_hours = 0
    total_classes = 0
    total_before_tax = Decimal(0)
    total_after_tax = Decimal(0)

    for student in students:
        classes = Classes.objects.filter(
            student=student,
            date__month=selected_date.month,
            date__year=selected_date.year,
        )

        if classes.exists():
            # student_hours = (
            #     classes.aggregate(total_hours=Sum("number_class_hours"))["total_hours"]
            #     or 0
            # )
            student_hours = (
                classes.aggregate(
                    total_hours=Sum(Cast("number_class_hours", IntegerField()))
                )["total_hours"]
                or 0
            )
            student_classes = classes.count()
            student_before_tax = student_hours * student.hourly_salary
            student_after_tax = student_before_tax * (1 - tax_percentage / 100)
        else:
            student_hours = 0
            student_classes = 0
            student_before_tax = 0.0
            student_after_tax = 0.0

        student.total_hours = student_hours // 60
        student.total_classes = student_classes
        student.total_before_tax = student_before_tax / 60
        student.total_after_tax = student_after_tax / 60

        total_hours += student.total_hours
        total_classes += student.total_classes
        total_before_tax += Decimal(student.total_before_tax)
        total_after_tax += Decimal(student.total_after_tax)

    return render(
        request,
        "dashboard/family_invoice_detail.html",
        {
            "family": family,
            "students": students,
            "tax_percentage": tax_percentage,
            "selected_month": selected_date,
            "total_hours": total_hours,
            "total_classes": total_classes,
            "total_before_tax": total_before_tax,
            "total_after_tax": total_after_tax,
        },
    )


def student_invoice_details(request, student_id):
    student = get_object_or_404(Student, pk=student_id, is_active=True)
    classes = Classes.objects.filter(student=student)

    current_date = datetime.now().date()
    
    try:
        billing_month = BillingMonths.objects.get(family=student.family)
        selected_date = billing_month.date
    except BillingMonths.DoesNotExist:
        selected_date = None

    if not selected_date:
        current_date = datetime.now().date()
        selected_date = current_date.replace(day=1)

    # Get the latest tax percentage
    latest_tax = Tax.objects.latest("date")
    tax_percentage = latest_tax.percentage if latest_tax else 0.0

    # Calculate totals for the student for the current month
    total_hours = (
        classes.filter(
            date__month=current_date.month, date__year=current_date.year
        ).aggregate(total_hours=Sum("number_class_hours"))["total_hours"]
        or 0
    )
    total_classes = classes.filter(
        date__month=current_date.month, date__year=current_date.year
    ).count()
    total_before_tax = total_hours * student.hourly_salary / 60
    total_after_tax = total_before_tax * (1 - tax_percentage / 100)

    return render(
        request,
        "dashboard/student_invoice_detail.html",
        {
            "student": student,
            "classes": classes,
            "total_hours": total_hours // 60,
            "total_classes": total_classes,
            "total_before_tax": total_before_tax,
            "total_after_tax": total_after_tax,
            "tax_percentage": tax_percentage,
            "selected_month": selected_date,
        },
    )


@login_required
def instructor_invoices(request):
    if not request.user.type == "Admin":
        return redirect("dash:dashboard")

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

    instructor_ids_with_classes = (
        Classes.objects.filter(date__range=[start_date, end_date])
        .values_list("instructor_id", flat=True)
        .distinct()
    )
    instructors = Instructor.objects.filter(
        user__is_active=True, id__in=instructor_ids_with_classes
    )

    # Calculate overall totals for the selected month (for admins only)
    overall_totals = (
        Classes.get_overall_totals(start_date, end_date)
    )

    total_hours = overall_totals["total_hours"] // 60

    # Calculate instructor totals for the selected month
    instructor_totals = {
        instructor.id: Classes.get_instructor_totals(instructor, start_date, end_date)
        for instructor in instructors
    }

    # Calculate overall total salary for all instructors
    overall_instructor_salary = sum(
        total["total_salary"] for total in instructor_totals.values()
    )

    return render(
        request,
        "dashboard/instructor_invoices.html",
        {
            "instructors": instructors,
            "instructor_totals": instructor_totals,
            "current_date": current_date,
            "overall_totals": overall_totals,
            "invoices": invoices,
            "overall_instructor_salary": overall_instructor_salary,
            "total_hours": total_hours,
        },
    )


@login_required
def marketer_commission_view(request):
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

    marketers = CustomUser.objects.filter(type=UserType.MARKETER, is_active=True)

    commissions = []

    for marketer in marketers:
        # Get all students who registered through this marketer
        marketer_students = Marketer_Student.objects.filter(marketer=marketer)

        total_commission = Decimal(0)

        for ms in marketer_students:
            student = ms.student
            # Calculate total salary for the student within the selected date range
            student_totals = Classes.get_family_totals(
                student.family, start_date, end_date
            )
            student_total_salary = student_totals["total_salary"]

            # Calculate the marketer's commission for this student
            commission = (marketer.marketer.ratio / 100) * student_total_salary
            total_commission += commission

        commissions.append({"marketer": marketer, "total_commission": total_commission})

    return render(
        request, "dashboard/marketer_invoices.html", {"commissions": commissions}
    )


def marketer_students(request):
    # Get the marketer object using the provided ID
    marketer_students = Marketer_Student.objects.filter(marketer=request.user)

    students = Student.objects.filter(id__in=marketer_students.values("student"))

    return render(
        request,
        "dashboard/student_the_marketer.html",
        {"students": students},
    )


@login_required
def instructor_invoices_detail(request):
    user = request.user

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

    # Filter invoices for the logged-in instructor
    invoices = Classes.objects.filter(
        instructor__user=user, date__range=[start_date, end_date]
    )

    # Calculate instructor totals for the logged-in instructor only
    instructor_totals = Classes.get_instructor_totals(user.instructor, start_date, end_date)

    return render(
        request,
        "dashboard/instructor-inv-detail.html",
        {
            "instructor_totals": instructor_totals,
            "current_date": current_date,
            "invoices": invoices,
        },
    )


# ------------------------------------------------ AdvancesDisc
@login_required
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
    return render(
        request,
        "dashboard/advancesdisc.html",
        {
            "form": form,
            "disc": disc,
        },
    )


def delete_disc(request, id):
    disc = Discounts.objects.get(id=id)
    disc.delete()
    messages.success(request, "تم حذف السلفة بنجاح!")
    return redirect("dash:advancesdisc")


@login_required
def invoices_link(request):
    if not request.user.type == "Admin":
        return redirect("dash:dashboard")

    families = Families.objects.filter(is_active=True)
    return render(request, "dashboard/invoices_link.html", {"families": families})


# ------------------------------------------------ Removed User


@login_required
def families_removed(request):
    families = Families.objects.filter(is_active=False)
    return render(request, "dashboard/families_removed.html", {"families": families})


@login_required
def instructor_removed(request):
    instructor = Instructor.objects.filter(user__is_active=False)
    return render(
        request, "dashboard/instructor_removed.html", {"instructor": instructor}
    )


# ------------------------------------------------ Active User
@login_required
def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"تم تفعيل المستخدم {user.name} بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def activate_family(request, user_id):
    user = get_object_or_404(Families, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"تم تفعيل المستخدم {user.name} بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


# ------------------------------------------------ Contact
@login_required
def contact(request):
    if not request.user.type == "Admin":
        return redirect("dash:dashboard")

    contacts = ContactUs.objects.all()
    return render(request, "dashboard/contact.html", {"contacts": contacts})


@login_required
def teacher_contact(request):
    if not request.user.type == "Admin":
        return redirect("dash:dashboard")

    contacts = TeacherContact.objects.all()
    return render(request, "dashboard/be_a_teacher.html", {"contacts": contacts})
