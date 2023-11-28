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


class University(models.Model):
    name = models.CharField(max_length=100, null=False,
                            blank=False, default="KPI")
    hyper_link = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=150, unique=True,
                            null=False, blank=False)
    postion = models.CharField(max_length=50)
    hyper_link = models.CharField(max_length=300, null=False, blank=False)
    university = models.ForeignKey(to=University, on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("detail_teacher", args=[str(self.pk)])


class Group(models.Model):
    name = models.CharField(max_length=15, unique=True)
    email = models.EmailField()
    university = models.ForeignKey(
        to=University, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("detail_group", args=[str(self.pk)])