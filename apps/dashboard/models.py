from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver


# ------------------------Settings
class Tax(models.Model):
    number = models.IntegerField(default=1)
    date = models.DateField(default=date.today)  # Automatically set to the current date

    def __str__(self):
        return str(self.number)


class BillingMonths(models.Model):
    date = models.DateField()

    def __str__(self):
        return self.date


# ------------------------People
class UserType(models.TextChoices):
    STUDENT = "Student", "طالب"
    INSTRUCTOR = "Instructor", "معلم"
    MANAGER = "Manager", "مشرف"
    FAMILIES = "Families", "عائله"
    ADMIN = "Admin", "ادمن"


class Gender(models.TextChoices):
    MALE = "Male", "ذكر"
    FEMALE = "Female", "انثى"


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("The Phone field must be set")
        phone = self.normalize_email(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(
        choices=UserType.choices, default=UserType.MANAGER, max_length=50
    )
    gender = models.CharField(
        choices=Gender.choices, max_length=10, null=True, blank=True
    )
    age = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name


class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - Manager"


@receiver(post_save, sender=CustomUser)
def create_manager_profile(sender, instance, created, **kwargs):
    if created and instance.type == UserType.MANAGER:
        Manager.objects.create(user=instance)


class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=250)
    hourly_salary = models.IntegerField(default=0)
    class_link = models.CharField(max_length=1000)
    manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, blank=True
    )
    id_number = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - Instructor"


class Families(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    the_state = models.CharField(max_length=250, null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True)
    payment_link = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.user.name} - Instructor"


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    family = models.ForeignKey(Families, on_delete=models.CASCADE)
    hourly_salary = models.IntegerField(default=0)
    payment_link = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.user.name} - Instructor"


class Instructor_Student(models.Model):
    family = models.ForeignKey(Families, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# ------------------------Registration of classes


class Evaluation(models.TextChoices):
    LOW = "Low", "ضعيف"
    GOOD = "Good", "مقبول"
    VGOOD = "Vgood", "جيد"
    EXCELLENCE = "Excellence", "امتياز"


class Class(models.Model):
    family = models.ForeignKey("Families", on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    instructor = models.ForeignKey("Instructor", on_delete=models.CASCADE)
    date = models.DateField()
    number_class_hours = models.IntegerField(default=0)
    evaluation = models.CharField(
        choices=Evaluation.choices, default=Evaluation.LOW, max_length=50
    )
    subject_name = models.CharField(max_length=300)
    nb = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Class on {self.date} by {self.instructor.user.name} for {self.student.user.name}"


# ------------------------Invoices


# ------------------------Advances and discounts


class Advances_Discounts(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    comment = models.CharField(max_length=250)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
