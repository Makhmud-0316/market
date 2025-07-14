from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LogInForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=150, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')
