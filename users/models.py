from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from pages.models import University
# Create your models here.


class CustomUser(AbstractUser):
    university = models.ForeignKey(
        to=University, on_delete=models.CASCADE, null=True, blank=True)
    is_stuff = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("home")
