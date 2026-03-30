from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .forms_password import FindPasswordForm, VerifyCodeForm, ResetPasswordForm
from .models import CustomUser
import random
from django.core.mail import send_mail

def find_password_view(request):
    step = request.session.get('step', 1)
    email = ''

    if request.method == 'POST':
        # 이메일 입력
        if 'send_code' in request.POST:
            email = request.POST.get('email')

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return render(request, 'find_password.html', {
                    'error': '등록된 이메일이 없습니다.',
                    'step': 1,
                    'email': email
                })

            import random
            code = str(random.randint(100000, 999999))

            request.session['find_pw_email'] = email
            request.session['find_pw_code'] = code
            request.session['step'] = 2

            from django.core.mail import send_mail
            send_mail(
                '인증코드',
                f'인증번호: {code}',
                None,
                [email],
                fail_silently=False,
            )

            return render(request, 'find_password.html', {
                'message': '인증번호가 전송되었습니다.',
                'step': 2,
                'email': email
            })

        # 인증번호 확인
        elif 'verify_code' in request.POST:
            input_code = request.POST.get('code')
            real_code = request.session.get('find_pw_code')
            email = request.session.get('find_pw_email', '')

            if input_code == real_code:
                request.session['pw_reset_ok'] = True
                request.session['step'] = 1  # 초기화
                return redirect('reset_password')
            else:
                return render(request, 'find_password.html', {
                    'error': '인증번호가 틀렸습니다.',
                    'step': 2,
                    'email': email
                })

    email = request.session.get('find_pw_email', '')
    return render(request, 'find_password.html', {'step': step, 'email': email})

def reset_password_view(request):
    if not request.session.get('pw_reset_ok'):
        return redirect('find_password')
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            pw1 = form.cleaned_data['new_password1']
            pw2 = form.cleaned_data['new_password2']
            if pw1 != pw2:
                return render(request, 'change_password.html', {'form': form, 'error': '비밀번호가 일치하지 않습니다.'})
            email = request.session.get('find_pw_email')
            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(pw1)
                user.save()
                for k in ['find_pw_email', 'find_pw_code', 'pw_reset_ok']:
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
