from django.db import models


class Slider(models.Model):
    img = models.ImageField(upload_to="slider/img/")
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Sliders"
        
    def __str__(self):
        return self.title


class Settings(models.Model):
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    whatsapp = models.CharField(max_length=12, blank=True, null=True)
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="images/logo", blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phones = models.CharField(max_length=100, blank=True, null=True)
    map_link = models.URLField(blank=True, null=True)
    text = models.TextField()
    video = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural = "Settings"

    def __str__(self):
        return "Settings"


class Pricing_Content(models.Model):
    content = models.TextField()

    class Meta:
        verbose_name_plural = "Pricing Content"

    def __str__(self):
        return self.content


class Pricing(models.Model):
    char = models.CharField(max_length=2, unique=True)
    week = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    classes = models.IntegerField()
    hours = models.IntegerField()

    class Meta:
        verbose_name_plural = "Pricing"

    def __str__(self):
        return self.char


class Fees(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Fees"

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=16)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact us"

    def __str__(self):
        return self.name


class TeacherContact(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    subject = models.CharField(max_length=200)
    qualifications = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Teacher Contact"

    def __str__(self):
        return self.full_name


class Tutors(models.Model):
    full_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="tutors/img/")
    qualifications = models.TextField()

    class Meta:
        verbose_name_plural = "Tutors"

    def __str__(self):
        return self.full_name


class MinClass(models.TextChoices):
    MIN30 = "min30", "30 Min"
    MIN45 = "min45", "45 Min"
    MIN60 = "min60", "60 Min"


class Plan(models.TextChoices):
    A = "A", "A"
    B = "B", "B"
    C = "C", "C"
    D = "D", "D"


class PriceContact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, unique=True)

    # Use the full choices from the MinClass and Plan enums
    min_class = models.CharField(choices=MinClass.choices, max_length=15)
    plan = models.CharField(choices=Plan.choices, max_length=2)

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
