from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('이미 사용 중인 아이디입니다.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 사용 중인 이메일입니다.')
        return email

    user_id = forms.CharField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'signup-input',
            'placeholder': '닉네임'
        })
    )

    username = forms.CharField(
        label='',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'signup-input',
            'placeholder': '아이디'
        })
    )

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'signup-input',
            'placeholder': '이메일'
        })
    )

    phone_number = forms.CharField(
    label='',
    max_length=20,
    widget=forms.TextInput(attrs={
        'class': 'signup-input',
        'placeholder': '전화번호'
    })
    )

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'signup-input',
            'placeholder': '비밀번호'
        }),
        help_text=''
    )

    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'signup-input',
            'placeholder': '비밀번호 확인'
        }),
        help_text=''
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_id', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = ''
            field.widget.attrs.update({'class': 'signup-input'})

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'login-input',
            'placeholder': '아이디'
        })
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'login-input',
            'placeholder': '비밀번호'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = ''
            field.widget.attrs.update({'class': 'login-input'})