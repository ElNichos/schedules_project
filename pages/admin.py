from django.contrib import admin

from .models import Teacher, Group, DayOfWeek, University
# Register your models here.

admin.site.register((Teacher, Group, DayOfWeek, University))
