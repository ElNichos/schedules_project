from django.db import models
from django.urls import reverse

# Create your models here.


class DayOfWeek(models.Model):
    name = models.CharField(max_length=20)
    order_number = models.PositiveIntegerField(
        unique=True, null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("", args=[str(self.pk)])


class Teacher(models.Model):
    name = models.CharField(max_length=150, unique=True,
                            null=False, blank=False)
    postion = models.CharField(max_length=50)
    hyper_link = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("", args=[str(self.pk)])


class Group(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("", args=[str(self.pk)])


class Lesson(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    hyper_link = models.CharField(max_length=300, null=False, blank=False)
    lesson_type = models.CharField(max_length=100, null=False, blank=False)

    day = models.ForeignKey(
        to=DayOfWeek, on_delete=models.CASCADE, related_name='day')
    num_lesson = models.PositiveIntegerField(null=False, blank=False)
    num_week = models.PositiveIntegerField(null=False, blank=False)
    is_session = models.BooleanField(null=False, blank=False)
    group = models.ManyToManyField(to=Group)
    teacher = models.ManyToManyField(to=Teacher)

    def __str__(self) -> str:
        return f"{self.num_lesson}/{self.day}/{self.num_week}|{self.title[:15]}"

    def get_absolute_url(self):
        return reverse("", args=[str(self.pk)])
