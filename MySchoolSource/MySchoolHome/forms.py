from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class CreateUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password1']
