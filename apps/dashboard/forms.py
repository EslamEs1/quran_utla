from django import forms
from .models import CustomUser, Instructor, Families, Student, Gender


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
