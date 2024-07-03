from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import (
    BaseUserForm,
    InstructorForm,
    FamiliesForm,
    StudentForm,
    Instructor_StudentForm,
    ClassesForm,
    BootstrapPasswordChangeForm,
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
        instructor_form = FamiliesForm()

    context = {
        "base_form": base_form,
        "instructor_form": instructor_form,
        "instructor": instructor,
    }
    return render(request, "dashboard/instructor.html", context)


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
        "families": families,
    }
    return render(request, "dashboard/families.html", context)


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
    }
    return render(request, "dashboard/student.html", context)


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
    return render(request, "dashboard/change_password.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            phone = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, phone=phone, password=password)
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
            messages.error(request, "ربما هناك حقول فارغة او لا يوجد معلم مرتبط بهذا الطالب")
    else:
        form = ClassesForm()

    context = {
        "form": form,
        "classes": classes_list,
    }
    return render(request, "dashboard/classes.html", context)
