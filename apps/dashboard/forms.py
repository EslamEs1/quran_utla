from django import forms
from django.contrib.auth import get_user_model
from .models import (
    Instructor,
    Families,
    Student,
    Instructor_Student,
    Classes,
    Discounts,
    Marketer_Student,
    UserType,
    Manager,
    Marketer
)
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.formfields import PhoneNumberField

CustomUser = get_user_model()


class BaseUserForm(forms.ModelForm):
    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "كلمة المرور"}
        ),
    )
    phone = forms.CharField(
        label="رقم الهاتف",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "رقم الهاتف"}
        ),
        validators=[
            RegexValidator(
                regex=r"^\d{10,}$",
                message="يجب أن يحتوي رقم الهاتف على 10 أرقام على الأقل",
                code="invalid_phone",
            )
        ],
    )
    name = forms.CharField(
        label="الاسم",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "الاسم"}),
    )
    address = forms.CharField(
        label="العنوان",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "العنوان"}
        ),
    )
    gender = forms.ChoiceField(
        label="الجنس",
        choices=[
            ("Male", "ذكر"),
            ("Female", "انثي"),
        ],  # Update with your actual choices
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "الجنس"}),
    )
    age = forms.IntegerField(
        label="العمر",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "العمر"}
        ),
        validators=[
            RegexValidator(
                regex=r"^\d{1,2}$",
                message="يجب أن يكون العمر رقمًا من خانة أو خانتين",
                code="invalid_age",
            )
        ],
    )

    class Meta:
        model = CustomUser
        fields = ["phone", "password", "name", "address", "gender", "age"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Ensure password is hashed
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="رقم الهاتف",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "رقم الهاتف"}
        ),
    )
    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "كلمة المرور"}
        ),
    )


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = [
            "manager",
            "qualification",
            "hourly_salary",
            "class_link",
            "id_number",
        ]
        widgets = {
            "qualification": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "المؤهل"}
            ),
            "hourly_salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "الراتب بالساعه"}
            ),
            "class_link": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "رابط الحصة",
                }
            ),
            "id_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "رقم الهوية",
                }
            ),
            "manager": forms.Select(
                attrs={"class": "form-control", "placeholder": "المشرف"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(InstructorForm, self).__init__(*args, **kwargs)

        if user and user.type == UserType.MANAGER:
            try:
                manager_instance = Manager.objects.get(user=user)
                self.fields["manager"].widget = forms.HiddenInput()
                self.fields["manager"].initial = manager_instance.pk
            except Manager.DoesNotExist:
                self.fields["manager"].widget = forms.HiddenInput()
                self.fields["manager"].initial = None

        self.fields["qualification"].label = "المؤهل"
        self.fields["hourly_salary"].label = "الراتب بالساعه"
        self.fields["class_link"].label = "رابط الحصه"
        self.fields["id_number"].label = "رقم الهويه"
        self.fields["manager"].label = "المشرف"


class FamiliesForm(forms.ModelForm):
    number = PhoneNumberField()
    class Meta:
        model = Families
        fields = [
            "name",
            "number",
            "manager",
            "address",
            "gender",
            "the_state",
            "payment_link",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "الأسم"}
            ),
            "number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "رقم الهاتف"}
            ),
            "manager": forms.Select(
                attrs={"class": "form-control", "placeholder": "المشرف"}
            ),
            "gender": forms.Select(
                attrs={"class": "form-control", "placeholder": "الجنس"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "العنوان"}
            ),
            "the_state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "الولاية"}
            ),
            "payment_link": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "رابط الدفع"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(FamiliesForm, self).__init__(*args, **kwargs)

        if user and user.type == UserType.MANAGER:
            try:
                manager_instance = Manager.objects.get(user=user)
                self.fields["manager"].widget = forms.HiddenInput()
                self.fields["manager"].initial = manager_instance.pk
            except Manager.DoesNotExist:
                self.fields["manager"].widget = forms.HiddenInput()
                self.fields["manager"].initial = None

        self.fields["name"].label = "الأسم"
        self.fields["number"].label = "رقم الهاتف"
        self.fields["manager"].label = "المشرف"
        self.fields["gender"].label = "الجنس"
        self.fields["address"].label = "العنوان"
        self.fields["the_state"].label = "الولاية"
        self.fields["payment_link"].label = "رابط الدفع"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["family", "name", "gender", "age", "hourly_salary", "payment_link"]
        widgets = {
            "family": forms.Select(
                attrs={"class": "form-control", "placeholder": "العائلة"}
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "الأسم"}
            ),
            "gender": forms.Select(
                attrs={"class": "form-control", "placeholder": "الجنس"}
            ),
            "age": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "العمر"}
            ),
            "hourly_salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "السعر بالساعه"}
            ),
            "payment_link": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "رابط الدفع"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields["family"].label = "العائلة"
        self.fields["name"].label = "الأسم"
        self.fields["gender"].label = "الجنس"
        self.fields["age"].label = "العمر"
        self.fields["hourly_salary"].label = "السعر بالساعه"
        self.fields["payment_link"].label = "رابط الدفع"


class MarketerForm(forms.ModelForm):
    class Meta:
        model = Marketer
        fields = ["ratio", "salary"]
        widgets = {
            "salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "المرتب"}
            ),
            "ratio": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "النسبة"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MarketerForm, self).__init__(*args, **kwargs)
        self.fields["salary"].label = "المرتب"
        self.fields["ratio"].label = "نسبة الفاتورة"


class Instructor_StudentForm(forms.ModelForm):
    class Meta:
        model = Instructor_Student
        fields = ["family", "student", "instructor"]
        widgets = {
            "family": forms.Select(
                attrs={
                    "class": "form-control selectpicker",
                    "id": "id_family",
                    "data-show-subtext": "true",
                }
            ),
            "student": forms.Select(
                attrs={
                    "class": "form-control selectpicker",
                    "id": "id_student",
                    "data-show-subtext": "true",
                }
            ),
            "instructor": forms.Select(
                attrs={
                    "class": "form-control selectpicker",
                    "data-show-subtext": "true",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(Instructor_StudentForm, self).__init__(*args, **kwargs)
        self.fields["family"].label = "العائله"
        self.fields["student"].label = "الطالب"
        self.fields["instructor"].label = "المعلم"

        if "family" in self.data:
            try:
                family_id = str(self.data.get("family"))
                self.fields["student"].queryset = Student.objects.filter(
                    family_id=family_id, is_active=True
                ).order_by("name")
            except (ValueError, TypeError):
                self.fields["student"].queryset = Student.objects.none()
        elif self.instance.pk:
            self.fields["student"].queryset = self.instance.family.student_set.order_by(
                "name"
            )
        else:
            self.fields["student"].queryset = Student.objects.none()


class ClassesForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = [
            "family",
            "student",
            "instructor",
            "date",
            "number_class_hours",
            "evaluation",
            "subject_name",
            "notes",
        ]
        widgets = {
            "family": forms.Select(
                attrs={"class": "form-control", "placeholder": "العائلة"}
            ),
            "student": forms.Select(
                attrs={"class": "form-control", "placeholder": "الطالب"}
            ),
            "instructor": forms.Select(
                attrs={"class": "form-control", "placeholder": "المعلم"}
            ),
            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "placeholder": "تاريخ الحصة",
                    "type": "date",
                },
            ),
            "number_class_hours": forms.Select(
                attrs={"class": "form-control", "placeholder": "عدد ساعات الحصة"}
            ),
            "evaluation": forms.Select(
                attrs={"class": "form-control", "placeholder": "التقييم"}
            ),
            "subject_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "أسم الماده"}
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "ملحوظة"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ClassesForm, self).__init__(*args, **kwargs)

        if user and user.type == UserType.INSTRUCTOR:
            try:
                instructor_instance = Instructor.objects.get(user=user)

                # Filter families to include only those associated with the instructor
                family_ids = Instructor_Student.objects.filter(
                    instructor=instructor_instance
                ).values_list("family", flat=True)
                self.fields["family"].queryset = Families.objects.filter(
                    id__in=family_ids
                )

                # Automatically set the instructor and hide the field
                self.fields["instructor"].widget = forms.HiddenInput()
                self.fields["instructor"].initial = instructor_instance.pk

                # Set initial queryset for students based on the selected family
                if "family" in self.data:
                    try:
                        family_id = int(self.data.get("family"))
                        self.fields["student"].queryset = Student.objects.filter(
                            family_id=family_id,
                            id__in=Instructor_Student.objects.filter(
                                instructor=instructor_instance
                            ).values_list("student", flat=True),
                        ).order_by("name")
                    except (ValueError, TypeError):
                        self.fields["student"].queryset = Student.objects.none()
                elif self.instance.pk:
                    self.fields["student"].queryset = (
                        self.instance.family.student_set.filter(
                            id__in=Instructor_Student.objects.filter(
                                instructor=instructor_instance
                            ).values_list("student", flat=True)
                        ).order_by("name")
                    )
                else:
                    self.fields["student"].queryset = Student.objects.none()

            except Instructor.DoesNotExist:
                self.fields["instructor"].widget = forms.HiddenInput()
                self.fields["instructor"].initial = None
                self.fields["family"].queryset = Families.objects.none()
                self.fields["student"].queryset = Student.objects.none()
        else:
            self.fields["family"].queryset = Families.objects.none()
            self.fields["student"].queryset = Student.objects.none()

        # Set labels for form fields
        self.fields["family"].label = "العائلة"
        self.fields["instructor"].label = "المعلم"
        self.fields["student"].label = "الطالب"
        self.fields["date"].label = "تاريخ الحصة"
        self.fields["number_class_hours"].label = "عدد ساعات الحصة"
        self.fields["evaluation"].label = "التقييم"
        self.fields["subject_name"].label = "أسم الماده"
        self.fields["notes"].label = "ملحوظة"

    def save(self, commit=True):
        instance = super(ClassesForm, self).save(commit=False)

        # Automatically set the instructor based on the selected student
        student_id = self.cleaned_data.get("student")
        instructor_student = Instructor_Student.objects.filter(
            student_id=student_id
        ).first()

        if instructor_student:
            instance.instructor = instructor_student.instructor

        if commit:
            instance.save()

        return instance


class BootstrapPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "كلمة المرور القديمة"}
        )
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "كلمة المرور الجديدة"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "تأكيد كلمة المرور"}
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "رقم الهاتف"}
        ),
        label="رقم الهاتف",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "كلمة المرور"}
        ),
        label="كلمة المرور",
    )

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "رقم الهاتف"
        self.fields["password"].label = "كلمة المرور"


class AdminPasswordChangeForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "رقم الهاتف"}
        ),
        label="رقم الهاتف",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "كلمة المرور الجديدة"}
        ),
        label="كلمة المرور الجديدة",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "تأكيد كلمة المرور الجديدة"}
        ),
        label="تأكيد كلمة المرور الجديدة",
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("كلمتا المرور غير متطابقتين.")

        return cleaned_data

    def save(self, commit=True):
        phone = self.cleaned_data["phone"]
        new_password = self.cleaned_data["new_password1"]

        try:
            user = CustomUser.objects.get(phone=phone)
            user.set_password(new_password)
            if commit:
                user.save()
            return user
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("المستخدم بهذا الرقم غير موجود.")


class DiscountsForm(forms.ModelForm):
    class Meta:
        model = Discounts
        fields = "__all__"
        widgets = {
            "instructor": forms.Select(
                attrs={"class": "form-control", "placeholder": "المعلم"}
            ),
            "marketer": forms.Select(
                attrs={"class": "form-control", "placeholder": "المسوق"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "المبلغ"}
            ),
            "comment": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "تعليق"}
            ),
            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "placeholder": "التاريخ",
                    "type": "date",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super(DiscountsForm, self).__init__(*args, **kwargs)
        self.fields["instructor"].label = "المعلم"
        self.fields["marketer"].label = "المسوق"
        self.fields["amount"].label = "المبلغ"
        self.fields["comment"].label = "تعليق"
        self.fields["date"].label = "التاريخ"

    def clean(self):
        cleaned_data = super().clean()
        instructor = cleaned_data.get("instructor")
        marketer = cleaned_data.get("marketer")

        if not instructor and not marketer:
            raise forms.ValidationError("الرجاء اختيار إما مدرب أو مسوق.")

        # Set the field not selected to None
        if instructor:
            cleaned_data["marketer"] = None
        if marketer:
            cleaned_data["instructor"] = None

        return cleaned_data


class Marketer_StudentForm(forms.ModelForm):
    class Meta:
        model = Marketer_Student
        fields = ["family", "student", "marketer"]
        widgets = {
            "family": forms.Select(attrs={"class": "form-control", "id": "id_family"}),
            "student": forms.Select(
                attrs={"class": "form-control", "id": "id_student"}
            ),
            "marketer": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(Marketer_StudentForm, self).__init__(*args, **kwargs)
        self.fields["family"].label = "العائله"
        self.fields["student"].label = "الطالب"
        self.fields["marketer"].label = "المسوق"

        if "family" in self.data:
            try:
                family_id = str(self.data.get("family"))
                self.fields["student"].queryset = Student.objects.filter(
                    family_id=family_id, is_active=True
                ).order_by("name")
            except (ValueError, TypeError):
                self.fields["student"].queryset = Student.objects.none()
        elif self.instance.pk:
            self.fields["student"].queryset = self.instance.family.student_set.order_by(
                "name"
            )
        else:
            self.fields["student"].queryset = Student.objects.none()
