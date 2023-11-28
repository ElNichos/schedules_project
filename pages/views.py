from collections import deque
from typing import Any


from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

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

GROUP_TEMPLATES = 'pages/group_crud/'
TEACHER_TEMPLATES = 'pages/teacher_crud/'
PAGES_TEMPLATES = 'pages/schedules_views_tempaltes/'

global SCHEDULES_TO_REDIRECT
SCHEDULES_TO_REDIRECT = ''

def get_current_day_lesson():
    pass

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


def get_group_view(request: HttpRequest):
    print(f"***{PAGES_TEMPLATES}***")
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
    pass


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
