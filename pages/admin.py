from django.contrib import admin

from .models import Teacher, Lesson, Group, DayOfWeek
# Register your models here.

admin.site.register((Lesson, Teacher, Group, DayOfWeek))
