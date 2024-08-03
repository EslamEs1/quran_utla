from django.db import models


class About(models.Model):
    content = models.TextField()
    url = models.URLField()

    # Metadata
    def __str__(self):
        return self.content


class WhyUs(models.Model):
    img = models.ImageField(upload_to="whyus/img/")
    name = models.CharField(max_length=150)
    content = models.TextField()

    # Metadata
    def __str__(self):
        return self.name


class Testimonials(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)

    # Metadata
    def __str__(self):
        return self.name


class How_it_works(models.Model):
    content = models.TextField()

    # Metadata
    def __str__(self):
        return self.content


class Terms(models.Model):
    content = models.TextField()

    # Metadata
    def __str__(self):
        return self.content
