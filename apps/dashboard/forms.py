from django import forms
from .models import CustomUser, Manager, Instructor, Families, Student
from .models import Gender  # Import the Gender choices


class BaseUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(choices=Gender.choices, widget=forms.Select(attrs={"class": "form-control"}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = ["phone", "name", "address", "gender", "age", "password"]


class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = []  # Manager does not have additional fields beyond CustomUser


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
            "qualification": forms.TextInput(attrs={"class": "form-control"}),
            "hourly_salary": forms.NumberInput(attrs={"class": "form-control"}),
            "class_link": forms.URLInput(attrs={"class": "form-control"}),
            "id_number": forms.TextInput(attrs={"class": "form-control"}),
            "manager": forms.Select(attrs={"class": "form-control"}),
        }


class FamiliesForm(forms.ModelForm):
    class Meta:
        model = Families
        fields = ["the_state", "id_number", "payment_link"]
        widgets = {
            "the_state": forms.TextInput(attrs={"class": "form-control"}),
            "id_number": forms.TextInput(attrs={"class": "form-control"}),
            "payment_link": forms.URLInput(attrs={"class": "form-control"}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["family", "hourly_salary", "payment_link"]
        widgets = {
            "family": forms.Select(attrs={"class": "form-control"}),
            "hourly_salary": forms.NumberInput(attrs={"class": "form-control"}),
            "payment_link": forms.URLInput(attrs={"class": "form-control"}),
        }
