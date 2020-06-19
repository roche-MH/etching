from django.contrib.auth import authenticate, login #인증관련
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout as DJ_logout
from .forms import SignupForm, LoginForm, ProfileForm #같은 폴더안에 폼스 폴더를 만들고 signup 과 login를 정의해서 불러옴
from .models import Profile, Follow
import json
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.forms.utils import ErrorList
class DivErrorList(ErrorList):
     def __str__(self):
         return self.as_divs()
     def as_divs(self):
         if not self: return ''
         return '<div class="errorlist">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self])
def signup(request):
    if request.method =="POST":
        form = SignupForm(request.POST, request.FILES,error_class=DivErrorList)
        if form.is_valid(): # 값이 있는지 확인
            if form.clean_picture() == None:
                form.cleaned_data['picture']='accounts/noprofile.png'
                user = form.save() # 폼 내용 저장
            else:
                user = form.save()
            return redirect('accounts:login') #가입 되면 로그인으로 보냄
        else:
            return render(request, 'accounts/signup_fail.html',{"error" : form.errors})
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

@login_required
@require_POST
def follow(request):
    from_user = request.user.profile
    pk = request.POST.get('pk')
    to_user = get_object_or_404(Profile,pk=pk)
    follow, created = Follow.objects.get_or_create(from_user=from_user, to_user=to_user)

    if created:
        message = '팔로우 시작'
        status = 1
    else:
        follow.delete()
        message = '팔로우 취소'
        status = 0

    context = {
        'message': message,
        'status': status,
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def profile_edit(request, pk):
    user = get_object_or_404(Profile, pk=pk)
    if user.user != request.user:
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('post:post_list')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid(): # 값이 있다면
            user = form.save()
            #post.tag_set.clear()
            #post.tag_save()
            messages.success(request, '수정완료')
            return redirect('post:post_list')
    
    else:
        form = ProfileForm(instance=user)
    return render(request,  'accounts/profile_edit.html',{
        'post': user,
        'form': form,
    })
