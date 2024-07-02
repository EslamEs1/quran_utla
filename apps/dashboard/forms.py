from django import forms
from .models import CustomUser, Manager, Instructor, Families, Student
from .models import Gender  # Make sure to import Gender from your models


class BaseUserForm(forms.ModelForm):
    password = forms.CharField(
        label="",  # Empty label
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "كلمة المرور"}
        ),
    )
    phone = forms.CharField(
        label="",  # Empty label
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "رقم الهاتف"}
        ),
    )
    name = forms.CharField(
        label="",  # Empty label
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "الاسم"}),
    )
    address = forms.CharField(
        label="",  # Empty label
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "العنوان"}
        ),
    )
    gender = forms.ChoiceField(
        label="",  # Empty label
        choices=Gender.choices,
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "الجنس"}),
    )
    age = forms.IntegerField(
        label="",  # Empty label
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
            "qualification",
            "hourly_salary",
            "class_link",
            "id_number",
            "manager",
        ]
        widgets = {
            "qualification": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "المؤهل"}
            ),
            "hourly_salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "الراتب الساعي"}
            ),
            "class_link": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "رابط الصفحة"}
            ),
            "id_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "الرقم الوظيفي"}
            ),
            "manager": forms.Select(
                attrs={"class": "form-control", "placeholder": "المدير"}
            ),
        }


class FamiliesForm(forms.ModelForm):
    class Meta:
        model = Families
        fields = ["the_state", "id_number", "payment_link"]
        widgets = {
            "the_state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "الحالة"}
            ),
            "id_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "الرقم"}
            ),
            "payment_link": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "رابط الدفع"}
            ),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["family", "hourly_salary", "payment_link"]
        widgets = {
            "family": forms.Select(
                attrs={"class": "form-control", "placeholder": "العائلة"}
            ),
            "hourly_salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "الراتب الساعي"}
            ),
            "payment_link": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "رابط الدفع"}
            ),
        }
