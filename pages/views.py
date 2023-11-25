from collections import deque


from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse

from .models import (Teacher,
                     Group,
                     DayOfWeek,
                     University
                     )
from lessons.models import Lesson

# Create your views here.

global SCHEDULES_TO_REDIRECT
SCHEDULES_TO_REDIRECT = ''

def get_context(lessons: list, current_model: Group, session_flag: bool, university_id: int):

    lesson_time = {
        '1': '8.30',
        '2': '10.25',
        '3': '12.20',
        '4': '14.15',
        '5': '16.10',
        '6': '18.30',
    }
    lessons_tar = lessons.filter(university_id=university_id, is_session=session_flag)

    temp = []
    lesson_queryset = [deque(), deque()]
    for week in range(1, 3):
        lessons = lessons_tar.filter(num_week=week)

        for n_lesson in range(1, 7):
            temp_lessons = lessons.filter(num_lesson=n_lesson)

            temp += [lesson_time[str(n_lesson)]]

            for num_day in range(1, 7):
                try:
                    lesson = temp_lessons.get(day_id=num_day)
                    temp += [lesson]
                except (KeyError, Lesson.DoesNotExist):
                    temp += [None]

            lesson_queryset[week - 1].append(temp)
            temp = []
    context = {
        "university": University.objects.get(pk=university_id),
        "days": DayOfWeek.objects.all(),
        "current_model": current_model,
        "lessons": lesson_queryset,
        "weeks": range(1, 2),
        'is_session': str(session_flag),
    }
    return context


def get_group(request: HttpRequest):
    try:
        if request.GET["is_session"] == '2':
            is_session = True
        elif request.GET["is_session"] == '1':
            is_session = False

        university_id = University.objects.get(
            name=request.GET['university']).pk
        group = Group.objects.get(name=request.GET['group'])
        lessons = group.lesson_set.all()

    except (KeyError, Group.DoesNotExist, Lesson.DoesNotExist, University.DoesNotExist):
        return HttpResponse(render(request, template_name="pages/get_group_schedule.html",
                                   context={'groups_list': Group.objects.all(),
                                            'university_list': University.objects.all(),
                                            }))

    template = loader.get_template("pages/schedule_group.html")
    context = get_context(lessons, group, is_session, university_id)

    global SCHEDULES_TO_REDIRECT
    SCHEDULES_TO_REDIRECT = request.build_absolute_uri()

    return HttpResponse(template.render(context, request))


def get_teacher(request: HttpRequest):
    try:
        if request.GET["is_session"] == '2':
            is_session = True
        elif request.GET["is_session"] == '1':
            is_session = False

        university_id = University.objects.get(
            name=request.GET['university']).pk
        teacher = Teacher.objects.get(name=request.GET['teacher'])
        lessons = teacher.lesson_set.all()

    except (KeyError, Teacher.DoesNotExist, Lesson.DoesNotExist, University.DoesNotExist):
        return HttpResponse(render(request, template_name="pages/get_teacher_schedule.html",
                                   context={'groups_list': Group.objects.all(),
                                            'university_list': University.objects.all(),
                                            }))

    template = loader.get_template("pages/schedule_teacher.html")
    context = get_context(lessons, teacher, is_session, university_id)

    global SCHEDULES_TO_REDIRECT
    SCHEDULES_TO_REDIRECT = request.build_absolute_uri()

    return HttpResponse(template.render(context, request))


def get_uri():
    return SCHEDULES_TO_REDIRECT