from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    # homepage view
    path('', TemplateView.as_view(template_name="pages/schedules_views_tempaltes/home.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="pages/schedules_views_tempaltes/about.html"), name='about'),
    path('contacts/', TemplateView.as_view(template_name="pages/schedules_views_tempaltes/contacts.html"), name='contacts'),
   
    # schedules views for non-authenticated users
    path('group/', get_group_view, name='get_group'),
    path('teacher/', get_teacher_view, name='get_teacher'),
    path('search/', check_instanse_view, name='search_model'),
    path('table/', objects_table_view, name='get_table'),
    path('week_config/', week_config_view, name='week_config'),

    #group crud
    path('new_group/', CreateGroupView.as_view(), name='new_group'),
    path('<int:pk>/edit_group/', UpdateGroupView.as_view(), name='edit_group'),
    path('<int:pk>/detail_group/', DetailGroupView.as_view(), name='detail_group'),
    path('<int:pk>/delete_group/', DeleteGroupView.as_view(), name='delete_group'),

    #teacher crud
    path('new_teacher/', CreateTeacherView.as_view(), name='new_teacher'),
    path('<int:pk>/edit_teacher/', UpdateTeacherView.as_view(), name='edit_teacher'),
    path('<int:pk>/detail_teacher/', DetailTeacherView.as_view(), name='detail_teacher'),
    path('<int:pk>/delete_teacher/', DeleteTeacherView.as_view(), name='delete_teacher'),
]
