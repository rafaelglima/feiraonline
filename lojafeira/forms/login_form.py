from django.contrib.auth.forms import AuthenticationForm
from ..models import Usuario
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ['username', 'password']