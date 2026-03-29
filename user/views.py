from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .forms_password import FindPasswordForm, VerifyCodeForm, ResetPasswordForm
from .models import CustomUser
import random
def find_password_view(request):
    if request.method == 'POST':
        form = FindPasswordForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            try:
                user = CustomUser.objects.get(phone_number=phone)
            except CustomUser.DoesNotExist:
                return render(request, 'find_password.html', {'form': form, 'error': '등록된 전화번호가 없습니다.'})
            code = str(random.randint(100000, 999999))
            request.session['find_pw_phone'] = phone
            request.session['find_pw_code'] = code
            print(f"[인증번호] {code}")  # 실제 서비스에서는 문자로 전송
            return redirect('verify_code')
    else:
        form = FindPasswordForm()
    return render(request, 'find_password.html', {'form': form})

def verify_code_view(request):
    if 'find_pw_code' not in request.session:
        return redirect('find_password')
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == request.session.get('find_pw_code'):
                request.session['pw_reset_ok'] = True
                return redirect('reset_password')
            else:
                return render(request, 'verify_code.html', {'form': form, 'error': '인증번호가 일치하지 않습니다.'})
    else:
        form = VerifyCodeForm()
    return render(request, 'verify_code.html', {'form': form})

def reset_password_view(request):
    if not request.session.get('pw_reset_ok'):
        return redirect('find_password')
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            pw1 = form.cleaned_data['new_password1']
            pw2 = form.cleaned_data['new_password2']
            if pw1 != pw2:
                return render(request, 'reset_password.html', {'form': form, 'error': '비밀번호가 일치하지 않습니다.'})
            phone = request.session.get('find_pw_phone')
            try:
                user = CustomUser.objects.get(phone_number=phone)
                user.set_password(pw1)
                user.save()
                for k in ['find_pw_phone', 'find_pw_code', 'pw_reset_ok']:
                    if k in request.session:
                        del request.session[k]
                return redirect('login')
            except CustomUser.DoesNotExist:
                return redirect('find_password')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid(): # 유효성 검사 통과하면
            user = form.save()
            login(request, user)
            return redirect('login')  # 회원가입 후 로그인 페이지로 이동
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})
    # 회원가입 폼을 렌더링하여 넘김, 이 주소로 들어갔을 때 기본적 method는 get => 사용자에게 보여줌

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') # 로그인 후 홈 페이지로 이동
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'home.html')
