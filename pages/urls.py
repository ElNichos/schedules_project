from django.urls import path
from django.views.generic import TemplateView

from .views import get_group, get_teacher

urlpatterns = [
    path('', TemplateView.as_view(template_name="pages/home.html"), name='home'),
    path('group/', get_group, name='get_group'),
    path('teacher/', get_teacher, name='get_teacher'),
]
