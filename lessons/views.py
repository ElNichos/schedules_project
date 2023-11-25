from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user
from django.forms.models import BaseModelForm
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Lesson
from pages.models import DayOfWeek, Group, Teacher
from .forms import LessonCretionForm
from pages.views import get_uri

# Create your views here.

class DeleteLessonView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Lesson
    template_name = "lessons/delete_lesson.html"
    login_url = 'login'


    def get_success_url(self) -> str:
        return get_uri()


    def form_valid(self, form):
        super().form_valid(form)
        return redirect(get_uri())


class DetailLessonView(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    model = Lesson
    template_name = "lessons/detail_lesson.html"
    context_object_name = "lesson"
    login_url = 'login'
    

class UpdateLessonView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Lesson
    template_name = "lessons/update_lesson.html"
    fields = ['title', 'hyper_link', 'lesson_type', 'teacher',]
    login_url = 'login'


    def get_success_url(self) -> str:
        return get_uri()


    def form_valid(self, form):
        super().form_valid(form)
        return redirect(get_uri())

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class CreateLessonView(CreateView):
    model = Lesson
    form_class = LessonCretionForm 
    template_name = "lessons/new_lesson.html"
    login_url = 'login'


    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        request = self.request
        params = request.GET
        user = get_user(request)
        if not params:
            context = {
                 'author': user,
                 'university': user.university,
            }
        else:
            context = {
                'author': user,
                'university': user.university,
                'day' : DayOfWeek.objects.get(id = int(params['day_pk']) - 1),
                'num_lesson': params['num_lesson'],
                'num_week': params['num_week'],
                'is_session' : True if params['is_session'] == 'True' else False,
                # 'group' : Group.objects.get(id = params['group_pk']),
            }

            try:
                Group.objects.get(name = params['group'])
                Teacher.objects.get(name = params['teacher'])
            except Group.DoesNotExist:
                context.update({'teacher':Teacher.objects.get(name = params['teacher'])})
            except Teacher.DoesNotExist:
                context.update({'group':Group.objects.get(name = params['group'])})


        initial.update(context)
        return initial


    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = self.get_initial()
        return kwargs


    def form_invalid(self, form):
        messages.error(self.request, 'This lesson is already exists!\nTry again.')
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        return get_uri()


    def form_valid(self, form):
        super().form_valid(form)
        return redirect(get_uri())

    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
     
    