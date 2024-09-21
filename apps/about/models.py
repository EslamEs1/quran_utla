from django.db import models


class About(models.Model):
    content = models.TextField()
    url = models.URLField()

    # Metadata
    class Meta:
        verbose_name_plural = "About"

    def __str__(self):
        return self.content


class WhyUs(models.Model):
    img = models.ImageField(upload_to="whyus/img/")
    name = models.CharField(max_length=150)
    content = models.TextField()

    # Metadata
    class Meta:
        verbose_name_plural = "Why us"

    def __str__(self):
        return self.name


class Testimonials(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)

    # Metadata
    class Meta:
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name


class TestimonialsVideo(models.Model):
    url = models.URLField()

    # Metadata
    class Meta:
        verbose_name_plural = "Testimonials Video"

    def __str__(self):
        return self.url


class How_it_works(models.Model):
    content = models.TextField()

    # Metadata
    class Meta:
        verbose_name_plural = "How it works"

    def __str__(self):
        return self.content


class Terms(models.Model):
    content = models.TextField()

    # Metadata
    class Meta:
        verbose_name_plural = "Terms"

    def __str__(self):
        return self.content


class QuestionAnswer(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    
    # Metadata
    class Meta:
        verbose_name_plural = "Question & Answer"
    
    def __str__(self):
        return self.question
