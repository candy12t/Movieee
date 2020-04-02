from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import CustomUser


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'user_name', 'password1', 'password2')


class ProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'user_name', 'icon')