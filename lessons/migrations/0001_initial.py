# Generated by Django 4.2.6 on 2023-11-10 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0002_delete_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('hyper_link', models.CharField(max_length=300)),
                ('lesson_type', models.CharField(max_length=100)),
                ('num_lesson', models.PositiveIntegerField()),
                ('num_week', models.PositiveIntegerField()),
                ('is_session', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day', to='pages.dayofweek')),
                ('group', models.ManyToManyField(to='pages.group')),
                ('teacher', models.ManyToManyField(to='pages.teacher')),
                ('university', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pages.university')),
            ],
        ),
    ]
