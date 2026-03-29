from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):

    user_id = forms.CharField(label='아이디', max_length=30, required=True)
    username = forms.CharField(label='닉네임', max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_id', 'phone_number', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='닉네임')
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)