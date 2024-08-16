from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, F
from django.db.models.functions import Cast
import uuid
from phonenumber_field.modelfields import PhoneNumberField


# ------------------------Settings
class Tax(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    date = models.DateField(default=now)


class BillingMonths(models.Model):
    date = models.DateField()
    family = models.ForeignKey("Families", on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.date)} - {self.family}"


# ------------------------People
class UserType(models.TextChoices):
    MARKETER = "Marketer", "مسوق"
    INSTRUCTOR = "Instructor", "معلم"
    MANAGER = "Manager", "مشرف"
    ADMIN = "Admin", "ادمن"


class Gender(models.TextChoices):
    MALE = "Male", "ذكر"
    FEMALE = "Female", "انثى"


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The Phone field must be set")
        phone = self.normalize_email(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
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

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name


class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name}"


@receiver(post_save, sender=CustomUser)
def create_manager_profile(sender, instance, created, **kwargs):
    if created and instance.type == UserType.MANAGER:
        Manager.objects.create(user=instance)


class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=250)
    hourly_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class_link = models.CharField(max_length=1000, null=True, blank=True)
    manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, blank=True
    )
    id_number = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self):
        return self.user.name


class Families(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    number = PhoneNumberField()
    address = models.CharField(max_length=100)
    gender = models.CharField(choices=Gender.choices, max_length=10)
    the_state = models.CharField(max_length=250)
    manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, blank=True
    )
    payment_link = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Student(models.Model):
    family = models.ForeignKey(Families, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    gender = models.CharField(choices=Gender.choices, max_length=10)
    age = models.IntegerField()
    hourly_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_link = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Instructor_Student(models.Model):
    family = models.ForeignKey(Families, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Marketer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.user.name)


class Marketer_Student(models.Model):
    family = models.ForeignKey(Families, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marketer = models.ForeignKey(
        CustomUser,
        limit_choices_to={
            "type": UserType.MARKETER
        },  # Adjust UserType based on your definition
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


# ------------------------Registration of classes
class Evaluation(models.TextChoices):
    LOW = "Low", "ضعيف"
    GOOD = "Good", "مقبول"
    VGOOD = "Vgood", "جيد"
    EXCELLENCE = "Excellence", "امتياز"


class Duration(models.TextChoices):
    FORTY = "30", "30 دقيقة"
    FORTYFIVE = "45", "45 دقيقة"
    SIXTY = "60", "60 دقيقة"
    EIGHTY = "90", "90 دقيقة"
    NINETY = "120", "120 دقيقة"


class Classes(models.Model):
    family = models.ForeignKey(Families, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, blank=True, null=True
    )
    date = models.DateField()
    number_class_hours = models.CharField(
        choices=Duration.choices, default=Duration.FORTY, max_length=50
    )
    evaluation = models.CharField(
        choices=Evaluation.choices, default=Evaluation.LOW, max_length=50
    )
    subject_name = models.CharField(max_length=300)
    notes = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if self.instructor:
            return f"Class on {self.date} by {self.instructor.user.name} for {self.student.name}"
        else:
            return f"Class on {self.date} for {self.family.name}'s family"

    @staticmethod
    def get_overall_totals(start_date=None, end_date=None):
        queryset = Classes.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        total_sections = queryset.count()

        total_hours = queryset.aggregate(
            total_hours=Sum(Cast("number_class_hours", models.IntegerField()))
        )

        total_salary = (
            queryset.values("student")
            .annotate(
                total_salary=Sum(Cast("number_class_hours", models.DecimalField()))
                * F("student__hourly_salary")
                / 60
            )
            .aggregate(total_salary_sum=Sum("total_salary"))
        )

        return {
            "total_sections": total_sections,
            "total_hours": total_hours["total_hours"] or 0,
            "total_salary": total_salary["total_salary_sum"] or 0,
        }

    @staticmethod
    def get_family_totals(family, start_date=None, end_date=None):
        queryset = Classes.objects.filter(family=family)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        total_sections = queryset.count()

        total_hours = queryset.aggregate(
            total_hours=Sum(Cast("number_class_hours", models.IntegerField()))
        )

        total_salary = (
            queryset.values("student")
            .annotate(
                total_salary=Sum(Cast("number_class_hours", models.DecimalField()))
                * F("student__hourly_salary")
                / 60
            )
            .aggregate(total_salary_sum=Sum("total_salary"))
        )

        return {
            "family": family,
            "total_sections": total_sections,
            "total_hours": total_hours["total_hours"] // 60 or 0,
            "total_salary": total_salary["total_salary_sum"] or 0,
        }

    @staticmethod
    def get_instructor_totals(instructor, start_date=None, end_date=None):
        # Filter classes for the instructor within the date range
        queryset = Classes.objects.filter(instructor=instructor)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        # Calculate the total number of sections and hours
        total_sections = queryset.count()
        total_hours = queryset.aggregate(
            total_hours=Sum(Cast("number_class_hours", models.IntegerField()))
        )

        # Calculate the total salary for the instructor
        total_salary = (
            queryset.values("instructor")
            .annotate(
                total_salary=Sum(Cast("number_class_hours", models.DecimalField()))
                * F("instructor__hourly_salary")
                / 60
            )
            .aggregate(total_salary_sum=Sum("total_salary"))
        )

        # Calculate the total discounts for the instructor within the date range
        discount_queryset = Discounts.objects.filter(instructor=instructor)
        if start_date and end_date:
            discount_queryset = discount_queryset.filter(
                created_at__date__range=[start_date, end_date]
            )

        total_discounts = discount_queryset.aggregate(total_discounts=Sum("amount"))

        # Handle None values before calculation
        total_hours_value = total_hours["total_hours"] or 0

        # Subtract discounts from the total salary
        total_salary_after_discounts = (total_salary["total_salary_sum"] or 0) - (
            total_discounts["total_discounts"] or 0
        )

        return {
            "instructor": instructor,
            "total_sections": total_sections,
            "total_hours": total_hours_value // 60,
            "total_salary": total_salary_after_discounts,
            "total_discounts": total_discounts["total_discounts"] or 0,
        }


# ------------------------Advances and discounts
class Discounts(models.Model):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, null=True, blank=True
    )
    marketer = models.ForeignKey(
        Marketer, on_delete=models.CASCADE, null=True, blank=True
    )
    amount = models.IntegerField(default=0)
    comment = models.CharField(max_length=250)
    date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
