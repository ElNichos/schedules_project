from django.urls import path
from django.http import HttpRequest

from .views import (CreateLessonView,
                    DeleteLessonView,
                    UpdateLessonView,
                    DetailLessonView,
                    )

urlpatterns = [
    # CRUD for athenticated and authorized users
    path('new_lesson/', CreateLessonView.as_view(), name='new_lesson'),
    path('<int:pk>/', DetailLessonView.as_view(), name='detail_lesson'),
    path('<int:pk>/update/', UpdateLessonView.as_view(), name='update_lesson'),
    path('<int:pk>/delete/', DeleteLessonView.as_view(), name='delete_lesson'),
]
