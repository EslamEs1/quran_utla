from django.db import models


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

    class Meta:
        verbose_name_plural = "Settings"

    def __str__(self):
        return "Settings"


class Pricing_Content(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content


class Pricing(models.Model):
    char = models.CharField(max_length=2, unique=True)
    week = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    classes = models.IntegerField()
    hours = models.IntegerField()

    def __str__(self):
        return self.char


class Fees(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=16)
    message = models.TextField()

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
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name