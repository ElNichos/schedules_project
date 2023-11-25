from django.db import models

from pages.models import *
from users.models import CustomUser

# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    hyper_link = models.CharField(max_length=300, null=False, blank=False)
    lesson_type = models.CharField(max_length=100, null=False, blank=False)

    university = models.ForeignKey(
        to=University, on_delete=models.CASCADE, default=1)
    
    author = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    day = models.ForeignKey(
        to=DayOfWeek, on_delete=models.CASCADE, related_name='day')

    num_lesson = models.PositiveIntegerField(null=False, blank=False)
    num_week = models.PositiveIntegerField(null=False, blank=False)
    is_session = models.BooleanField(null=False, blank=False)
    group = models.ManyToManyField(to=Group)
    teacher = models.ManyToManyField(to=Teacher)

    def __str__(self) -> str:
        return f"{self.num_lesson}  {self.day}  {self.num_week}  |{self.title[:20]}"
    
    def get_absolute_url(self):
        return reverse("detail_lesson", kwargs={"pk": self.pk})
    