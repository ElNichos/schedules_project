from django.urls import path
from .views import SignUpView, ProfileEditView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('<int:pk>/update/', ProfileEditView.as_view(), name="edit_profile"),
]
