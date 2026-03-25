from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid(): # 유효성 검사 통과하면
            user = form.save()
            login(request, user)
            return redirect('signup')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})
    # 회원가입 폼을 렌더링하여 넘김, 이 주소로 들어갔을 때 기본적 method는 get => 사용자에게 보여줌
