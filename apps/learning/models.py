from django.db import models

# Create your models here.


class Curriculum(models.Model):
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Curriculum"

    def __str__(self):
        return self.description


class Methodology(models.Model):
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Methodology"

    def __str__(self):
        return self.description


class Steps_Methodology(models.Model):
    img = models.ImageField(upload_to="teaching/img/")
    name = models.CharField(max_length=150)
    content = models.TextField()

    class Meta:
        verbose_name_plural = "Steps Methodology"

    def __str__(self):
        return self.name


class Steps_To_Start(models.Model):
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Steps To Start"

    def __str__(self):
        return self.title


class Study_Plan(models.Model):
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Study Plan"

    def __str__(self):
        return self.title
