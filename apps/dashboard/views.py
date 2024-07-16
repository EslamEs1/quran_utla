from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomAuthenticationForm
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count, Q

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
    Contact,
    BillingMonths,
    Manager,
    Marketer_Student,
)


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
    current_date = datetime.now()
    billing = BillingMonths.objects.filter(
        date__month=current_date.month, date__year=current_date.year
    )
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
            & Q(is_active=True) & Q(type=UserType.MARKETER)
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
                Q(user__name__icontains=search_query)
                | Q(user__phone__icontains=search_query)
                | Q(user__address__icontains=search_query)
            )
            & Q(user__is_active=True)  # Correct placement of the '&' operator
        )
    else:
        families = Families.objects.filter(user__is_active=True)

    managers = CustomUser.objects.filter(type=UserType.MANAGER, is_active=True)
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
        "managers": managers,
        "search_query": search_query,
    }
    return render(request, "dashboard/families.html", context)


@login_required
def edit_family(request, id):
    custom_user = get_object_or_404(CustomUser, id=id)
    family = get_object_or_404(Families, user=custom_user)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        manager_id = request.POST.get("manager")
        the_state = request.POST.get("the_state")
        payment_link = request.POST.get("payment_link")

        if (
            name
            and phone
            and address
            and gender
            and age
            and manager_id
            and the_state
            and payment_link
        ):
            try:
                custom_user.name = name
                custom_user.phone = phone
                custom_user.address = address
                custom_user.gender = gender
                custom_user.age = age
                family.manager = Manager.objects.get(user__id=manager_id)
                family.the_state = the_state
                family.payment_link = payment_link
                custom_user.save()  # Save changes to CustomUser
                family.save()  # Save changes to Families

                messages.success(request, "تم تعديل العائلة بنجاح")
            except Manager.DoesNotExist:
                messages.error(request, "المشرف المحدد غير موجود أو ليس مشرفاً.")
        else:
            messages.error(request, "حدث خطأ أثناء تعديل العائلة")

    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def delete_family(request, id):
    family = get_object_or_404(CustomUser, id=id)
    family.is_active = False
    family.save()
    messages.success(request, "تم حذف العائلة بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


# ------------------------------------------------ Student
@login_required
def register_student(request):
    search_query = request.GET.get("search", "")
    if search_query:
        students = Student.objects.filter(
            (
                Q(user__name__icontains=search_query)
                | Q(user__phone__icontains=search_query)
                | Q(user__address__icontains=search_query)
            )
            & Q(user__is_active=True)  # Correct placement of the '&' operator
        )
    else:
        students = Student.objects.filter(user__is_active=True)

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
    custom_user = get_object_or_404(CustomUser, id=id)
    student = get_object_or_404(Student, user=custom_user)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        family_id = request.POST.get("family")
        payment_link = request.POST.get("payment_link")
        hourly_salary = request.POST.get("hourly_salary")

        if (
            name
            and phone
            and address
            and gender
            and age
            and family_id
            and hourly_salary
            and payment_link
        ):
            try:
                custom_user.name = name
                custom_user.phone = phone
                custom_user.address = address
                custom_user.gender = gender
                custom_user.age = age
                student.family = Families.objects.get(user__id=family_id)
                student.hourly_salary = hourly_salary
                student.payment_link = payment_link
                custom_user.save()  # Save changes to CustomUser
                student.save()  # Save changes to Families

                messages.success(request, "تم تعديل الطالب بنجاح")
            except Manager.DoesNotExist:
                messages.error(request, "المشرف المحدد غير موجود أو ليس مشرفاً.")
        else:
            messages.error(request, "حدث خطأ أثناء تعديل الطالب")

    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def delete_student(request, id):
    student = get_object_or_404(CustomUser, id=id)
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


# ------------------------------------------------ Login
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


# ------------------------------------------------ Student By Family
def get_students_by_family(request, family_id):
    students = Student.objects.filter(family_id=family_id).values("id", "user__name")
    return JsonResponse({"students": list(students)})


# ------------------------------------------------ Markter
@login_required
def register_marketer(request):
    search_query = request.GET.get("search", "")
    if search_query:
        marketer = CustomUser.objects.filter(
            (
                Q(name__icontains=search_query)
                | Q(phone__icontains=search_query)
                | Q(address__icontains=search_query)
            )
            & Q(is_active=True)
            & Q(type=UserType.MARKETER)
        )
    else:
        marketer = CustomUser.objects.filter(type=UserType.MARKETER, is_active=True)

    if request.method == "POST":
        base_form = BaseUserForm(request.POST)
        user_type = request.POST.get("user_type")
        if user_type and user_type == UserType.MARKETER:
            if base_form.is_valid():
                user = base_form.save(commit=False)
                user.type = UserType.MARKETER
                user.save()
                messages.success(request, "تم اضافة مسوق جديد بنجاح")
                return HttpResponseRedirect(request.headers.get("referer"))
            else:
                messages.error(request, "لم يتم الحفظ ربما رقم موجود من قبل")
    else:
        base_form = BaseUserForm()

    context = {
        "base_form": base_form,
        "marketer": marketer,
        "search_query": search_query,
    }
    return render(request, "dashboard/marketer.html", context)


@login_required
def edit_markter(request, id):
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

            messages.success(request, "تم تعديل المسوق بنجاح")
            return HttpResponseRedirect(request.headers.get("referer"))
        else:
            messages.error(request, "حدث خطأ أثناء تعديل المسوق")


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
    families = Families.objects.filter(user__is_active=True)

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
    family = get_object_or_404(Families, pk=family_id, user__is_active=True)
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
    student = get_object_or_404(Student, pk=student_id, user__is_active=True)
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
    instructors = Instructor.objects.filter(user__is_active=True)

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
    return render(
        request,
        "dashboard/advancesdisc.html",
        {
            "form": form,
            "disc": disc,
        },
    )


def invoices_link(request):
    families = Families.objects.filter(user__is_active=True)
    return render(request, "dashboard/invoices_link.html", {"families": families})


def families_removed(request):
    families = Families.objects.filter(user__is_active=False)
    return render(request, "dashboard/families_removed.html", {"families": families})


def instructor_removed(request):
    instructor = Instructor.objects.filter(user__is_active=False)
    return render(
        request, "dashboard/instructor_removed.html", {"instructor": instructor}
    )


def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"تم تفعيل المستخدم {user.name} بنجاح")
    return HttpResponseRedirect(request.headers.get("referer"))


def contact(request):
    contact = Contact.objects.all()
    return render(request, "dashboard/contact.html", {"contact": contact})
