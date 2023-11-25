from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser
from pages.models import University


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("university", "is_stuff")


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'university', 'is_stuff', )
