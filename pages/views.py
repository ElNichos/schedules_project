from collections import deque
from typing import Any

from django.contrib.auth import get_user
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import datetime, timedelta

from .models import (Teacher,
                     Group,
                     DayOfWeek,
                     University
                     )
from lessons.models import Lesson
from .forms import GroupCreationForm, TeacherCreationForm, UpdateTeacherForm, UpdateGroupForm

# Create your views here.

global GROUP_TEMPLATES
global TEACHER_TEMPLATES
global PAGES_TEMPLATES
global SCHEDULES_TO_REDIRECT
global NUM_WEEK

GROUP_TEMPLATES = 'pages/group_crud/'
TEACHER_TEMPLATES = 'pages/teacher_crud/'
PAGES_TEMPLATES = 'pages/schedules_views_tempaltes/'
SCHEDULES_TO_REDIRECT = ''
NUM_WEEK = 1

def week_config_view(request:HttpRequest):
    global NUM_WEEK
    NUM_WEEK = int(request.POST['week'])
    messages.success(request=request, message=f"Origin week is {NUM_WEEK}")
    return render(request, template_name="pages/schedules_views_tempaltes/home.html")


def get_current_day_lesson():
    current_day = datetime.now().strftime('%A')
    current_num_day = datetime.now().weekday() + 2
    if current_day == 'Sunday':
        global NUM_WEEK
        if NUM_WEEK == 2:
           NUM_WEEK = 1 
        else:
            NUM_WEEK += 1

    lesson_time = timedelta(hours=1, minutes=30 + 20)
    current_time = timedelta(hours=int(datetime.now().strftime('%H')), minutes=int(datetime.now().strftime('%M')))
    lesson_time = [
        [timedelta(hours=0), timedelta(hours=10, minutes=5)],
        [timedelta(hours=10, minutes=5), timedelta(hours=11, minutes=55)],
        [timedelta(hours=11, minutes=55), timedelta(hours=13, minutes=55)],
        [timedelta(hours=13, minutes=55), timedelta(hours=15, minutes=50)],
        [timedelta(hours=15, minutes=50), timedelta(hours=18, minutes=10)],
        [timedelta(hours=18, minutes=10), timedelta(hours=23, minutes=55)],
    ]
    for idx, [t_min, t_max] in enumerate(lesson_time):
        if (t_min <= current_time <= t_max):
            current_num_lesson = idx + 1
            break
    return (current_num_lesson, current_day, NUM_WEEK, current_num_day)
  

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
    current_num_lesson, _ , NUM_WEEK, current_num_day = get_current_day_lesson()
    context = {
        #schedules table
        "university": University.objects.get(pk=university_id),
        "days": DayOfWeek.objects.all(),
        "current_model": current_model,
        "lessons": lesson_queryset,
        "weeks": range(1, 2),
        'is_session': str(session_flag),
        #highlighting current time
        'current_num_lesson':current_num_lesson,
        'current_day':current_num_day,
        'NUM_WEEK':NUM_WEEK,
    }
    return context


def get_group_view(request: HttpRequest):
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
        return HttpResponse(render(request, template_name=PAGES_TEMPLATES + "get_group_schedule.html",
                                   context={'groups_list': Group.objects.all(),
                                            'university_list': University.objects.all(),
                                            }))
    
    template = loader.get_template(PAGES_TEMPLATES + "schedule_group.html")
    context = get_context(lessons, group, is_session, university_id)

    global SCHEDULES_TO_REDIRECT
    SCHEDULES_TO_REDIRECT = request.build_absolute_uri()

    return HttpResponse(template.render(context, request))


def get_teacher_view(request: HttpRequest):
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
        return HttpResponse(render(request, template_name=PAGES_TEMPLATES + "get_teacher_schedule.html",
                                   context={'groups_list': Group.objects.all(),
                                            'university_list': University.objects.all(),
                                            }))

    template = loader.get_template(PAGES_TEMPLATES + "schedule_teacher.html")
    context = get_context(lessons, teacher, is_session, university_id)

    global SCHEDULES_TO_REDIRECT
    SCHEDULES_TO_REDIRECT = request.build_absolute_uri()

    return HttpResponse(template.render(context, request))


def get_uri():
    if not SCHEDULES_TO_REDIRECT:
        return "/"
    else:
        return SCHEDULES_TO_REDIRECT


def check_instanse_view(request:HttpRequest):
    name = request.GET.get('name')
    model = request.GET.get('model')

    if model not in ['Group', 'Teacher']:
        messages.error(request, 'Incorrect input!\nTry again.')
    else:
        if model == 'Group':
            try:
                Group.objects.get(name=name)
            except Group.DoesNotExist:
                messages.error(request, f'Group {name} not found!')
            else:
                messages.success(request=request, message=f'Group {name} exists!')
        elif model == 'Teacher':    
            try:
                Teacher.objects.get(name=name)
            except Teacher.DoesNotExist:
                messages.error(request, f'Teacher {name}  not found!')
            else:
                messages.success(request=request, message=f'Teacher {name} exists!')
    return render(request, template_name="pages/schedules_views_tempaltes/home.html")


def objects_table_view(request:HttpRequest):
    model = request.GET.get('model')
    user = get_user(request=request)
    try:
        user.university
    except AttributeError:
        user.university = University.objects.get(pk=1)
    if model == 'Group':
        objects = Group.objects.filter(university = user.university)
    elif model == 'Teacher':    
        objects = Teacher.objects.filter(university = user.university)

    global SCHEDULES_TO_REDIRECT
    SCHEDULES_TO_REDIRECT = request.build_absolute_uri()

    return render(request, template_name="pages/schedules_views_tempaltes/object_table.html", context={'model':model, 'objects':objects,})


# group-model CRUD
class CreateGroupView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = GROUP_TEMPLATES + "new_group.html"
    login_url = 'login'
    form_class = GroupCreationForm
    
    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        context = {
            'university':self.request.user.university,
        }
        initial.update(context)
        return initial
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['initial'].update(self.get_initial())
        return kwargs
    
    def form_valid(self, form):
        super().form_valid(form)
        return redirect(get_uri())


class DetailGroupView(DetailView):
    model = Group
    template_name = GROUP_TEMPLATES + "detail_group.html"
    context_object_name = "group"


class DeleteGroupView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = GROUP_TEMPLATES + "delete_group.html"
    login_url = 'login'

    def get_success_url(self) -> str:
        return get_uri()

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(get_uri())


class UpdateGroupView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = GROUP_TEMPLATES + "update_group.html"
    login_url = 'login'
    context_object_name = 'group'
    form_class = UpdateGroupForm

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(get_uri())


# teacher-model CRUD
class CreateTeacherView(LoginRequiredMixin, CreateView):
    model = Teacher
    template_name = TEACHER_TEMPLATES + "new_teacher.html"
    login_url = 'login'
    form_class = TeacherCreationForm
    
    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        context = {
            'university':self.request.user.university,
        }
        initial.update(context)
        return initial
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['initial'].update(self.get_initial())
        return kwargs
    
    def form_valid(self, form):
        super().form_valid(form)
        return redirect(get_uri())


class DetailTeacherView(DetailView):
    model = Teacher
    template_name = TEACHER_TEMPLATES + "detail_teacher.html"
    context_object_name = "teacher"


class DeleteTeacherView(LoginRequiredMixin, DeleteView):
    model = Teacher
    template_name = TEACHER_TEMPLATES + "delete_teacher.html"
    login_url = 'login'

    def get_success_url(self) -> str:
        return get_uri()

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(get_uri())


class UpdateTeacherView(LoginRequiredMixin, UpdateView):
    model = Teacher
    template_name = TEACHER_TEMPLATES + "update_teacher.html"
    login_url = 'login'
    context_object_name = 'teacher'
    form_class = UpdateTeacherForm

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(get_uri())
