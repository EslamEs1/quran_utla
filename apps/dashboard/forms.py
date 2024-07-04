from django import forms
from django.contrib.auth import get_user_model
from .models import (
    Instructor,
    Families,
    Student,
    Gender,
    Instructor_Student,
    Classes,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm


CustomUser = get_user_model()


class BaseUserForm(forms.ModelForm):
    password = forms.CharField(
        label="كلمة المرور",  # Arabic label
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "كلمة المرور"}
        ),
    )
    phone = forms.CharField(
        label="رقم الهاتف",  # Arabic label
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "رقم الهاتف"}
        ),
    )
    name = forms.CharField(
        label="الاسم",  # Arabic label
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "الاسم"}),
    )
    address = forms.CharField(
        label="العنوان",  # Arabic label
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "العنوان"}
        ),
    )
    gender = forms.ChoiceField(
        label="الجنس",  # Arabic label
        choices=Gender.choices,
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "الجنس"}),
    )

    age = forms.IntegerField(
        label="العمر",  # Arabic label
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "العمر"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["name", "phone", "address", "gender", "age", "password"]


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
            "class_link": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "رابط الحصه"}
            ),
            "id_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "رقم الهويه"}
            ),
            "manager": forms.Select(
                attrs={"class": "form-control", "placeholder": "المشرف"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(InstructorForm, self).__init__(*args, **kwargs)
        self.fields["qualification"].label = "المؤهل"
        self.fields["hourly_salary"].label = "الراتب بالساعه"
        self.fields["class_link"].label = "رابط الحصه"
        self.fields["id_number"].label = "رقم الهويه"
        self.fields["manager"].label = "المشرف"


class FamiliesForm(forms.ModelForm):
    class Meta:
        model = Families
        fields = ["manager", "the_state", "payment_link"]
        widgets = {
            "manager": forms.Select(
                attrs={"class": "form-control", "placeholder": "المشرف"}
            ),
            "the_state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "الولاية"}
            ),
            "payment_link": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "رابط الدفع"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FamiliesForm, self).__init__(*args, **kwargs)
        self.fields["manager"].label = "المشرف"
        self.fields["the_state"].label = "الولاية"
        self.fields["payment_link"].label = "رابط الدفع"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["family", "hourly_salary", "payment_link"]
        widgets = {
            "family": forms.Select(
                attrs={"class": "form-control", "placeholder": "العائلة"}
            ),
            "hourly_salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "الراتب بالساعه"}
            ),
            "payment_link": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "رابط الدفع"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields["family"].label = "العائلة"
        self.fields["hourly_salary"].label = "الراتب بالساعه"
        self.fields["payment_link"].label = "رابط الدفع"


class Instructor_StudentForm(forms.ModelForm):
    class Meta:
        model = Instructor_Student
        fields = ["family", "student", "instructor"]
        widgets = {
            "family": forms.Select(attrs={"class": "form-control", "id": "id_family"}),
            "student": forms.Select(
                attrs={"class": "form-control", "id": "id_student"}
            ),
            "instructor": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(Instructor_StudentForm, self).__init__(*args, **kwargs)
        self.fields["family"].label = "العائله"
        self.fields["student"].label = "الطالب"
        self.fields["instructor"].label = "المعلم"

        if "family" in self.data:
            try:
                family_id = int(self.data.get("family"))
                self.fields["student"].queryset = Student.objects.filter(
                    family_id=family_id
                ).order_by("user__name")
            except (ValueError, TypeError):
                self.fields["student"].queryset = Student.objects.none()
        elif self.instance.pk:
            self.fields["student"].queryset = self.instance.family.student_set.order_by(
                "user__name"
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
            "instructor": forms.HiddenInput(),
            "date": forms.DateInput(
                format="%Y-%m-%d",  # Adjust date format if needed
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
        super(ClassesForm, self).__init__(*args, **kwargs)
        self.fields["family"].label = "العائلة"
        self.fields["student"].label = "الطالب"
        self.fields["date"].label = "تاريخ الحصة"
        self.fields["number_class_hours"].label = "عدد ساعات الحصة"
        self.fields["evaluation"].label = "التقييم"
        self.fields["subject_name"].label = "أسم الماده"
        self.fields["notes"].label = "ملحوظة"

        if "family" in self.data:
            try:
                family_id = int(self.data.get("family"))
                self.fields["student"].queryset = Student.objects.filter(
                    family_id=family_id
                ).order_by("user__name")
            except (ValueError, TypeError):
                self.fields["student"].queryset = Student.objects.none()
        elif self.instance.pk:
            self.fields["student"].queryset = self.instance.family.student_set.order_by(
                "user__name"
            )
        else:
            self.fields["student"].queryset = Student.objects.none()

    def save(self, commit=True):
        instance = super(ClassesForm, self).save(commit=False)

        # Retrieve the instructor for the selected student
        student_id = self.cleaned_data.get("student")
        instructor = Instructor_Student.objects.filter(student_id=student_id).first()

        if instructor:
            instance.instructor = instructor.instructor

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
