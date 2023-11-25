from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("")
    template_name = "registration/signup.html"

class ProfileEditView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "registration/edit_profile.html"