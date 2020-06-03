from django.contrib.auth import authenticate, login #인증관련
from django.shortcuts import redirect, render
from django.contrib.auth import logout as DJ_logout
from .forms import SignupForm, LoginForm #같은 폴더안에 폼스 폴더를 만들고 signup 과 login를 정의해서 불러옴

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid(): # 값이 있는지 확인
            user = form.save() # 폼 내용 저장
            return redirect('accounts:login') #가입 되면 로그인으로 보냄
    else:
        form = SignupForm()
        return render(request, 'accounts/signup.html', {
            'form':form,
        }) # 아니면 다시 사인업으로 보냄

def login_check(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        name = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(username=name, password=pwd) # DB 에서 확인

        if user is not None:
            login(request,user) # 맞다면 로그인
            return redirect('/')
        else:
            return render(request, 'accounts/login_fail.html') ## 실패면 실패로 보냄
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {"form":form}) #에러가 나면 로그인페이지 다시 보낸다.

def logout(request):
    DJ_logout(request)
    return redirect('/') #로그아웃 시켜주기