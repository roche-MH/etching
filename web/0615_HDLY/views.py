from django.contrib.auth import get_user_model #유저모델 가져오기
from django.shortcuts import get_object_or_404, render, redirect # 404 render 기능 불러오기
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Like, Comment, Tema #Post 모델 가져오기
from .forms import *
from django.contrib import messages # 메세지 불러오기
from django.views.generic.list import ListView
import json
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

from django.conf import settings
from flask import request as rq
from django.views.decorators.csrf import csrf_exempt
from BG_model import GAN_model as gm
from cv2 import cv2 
from werkzeug import secure_filename


################################ Image 처리 영역 ################################

@login_required
def image_input(request): # 이미지 업로드 하는 부분
    return render(request, 'post/imginput.html')

def image_process(request): # 모델에 이미지 넣어서 결과 받아오는 부분
    path = settings.BASE_DIR

    src_img = request.FILES['srcimg'] # src_img 저장
    src_name = str(src_img)
    src_path = open(path + '/post/static/img/'+src_name, "wb")
    for ch in src_img.chunks() :
        src_path.write(ch)
    src_path.close()

    ref_img = request.FILES['refimg'] # ref_img 저장
    ref_name = str(ref_img)
    ref_path = open(path + '/post/static/img/'+ref_name, "wb")
    for ch in ref_img.chunks() :
        ref_path.write(ch)
    ref_path.close()

    s_path = path + '/post/static/img/'+src_name
    r_path = path + '/post/static/img/'+ref_name
    result = gm.makeupout(s_path, r_path)

    cv2.imwrite(path + '/post/static/img/result_src.jpg', result[0])
    cv2.imwrite(path + '/post/static/img/result_makeup.jpg', result[1])

    return render(request, 'post/imgprocess.html',{
        'src_img':result[0],
        'result_img':result[1],
    })

@login_required
def image_output(request): # 결과 이미지 보고, text 입력해서 업로드 하는 부분
    return render(request, 'post/post_new.html')

################################ End Image & Model Linked ################################
##########################################################################################



################################ 추가 기능 처리 영역 ################################

@login_required
def face_ratio_in(request): # face ratio function input
    return render(request, 'post/faceRatioInput.html')

@login_required
def face_ratio_out(request): # face ratio function output
    
    '''
        여기 모델이랑 합치는 부분
    '''

    return render(request, 'post/faceRatioOutput.html')

@login_required
def personal_color_in(request): # personal color detection function input
    return render(request, 'post/personalColorInput.html')

@login_required
def personal_color_out(request): # personal color detection function output
    
    '''
        여기 모델이랑 합치는 부분
    '''

    return render(request, 'post/personalColorOutput.html')

################################ End Additional Functions ###########################
#####################################################################################



def post_detail(request, pk,tema=None):
    post = get_object_or_404(Post, pk=pk)
    #comment_form = CommentForm()
    return render(request, 'post/post_detail.html',{
        #'comment_form': comment_form,
        'post': post,
    })

def post_profile_pk(request, pk):
    post = get_object_or_404(Post, pk=pk)
    model = Post
    post_list = Post.objects.all()
    user =get_object_or_404(get_user_model(), id=pk)
    user_profile = user.profile
    #comment_form = CommentForm()

    return render(request, 'post/post_profile.html',{
        #'comment_form': comment_form,
        'post': post,
        'post_list': post_list,
        'user_profile':user_profile,
    })




def post_list(request):

    post_list = Post.objects.all()
    distinct_tema = set(Post.objects.values_list('tema',flat=True)) # tema 에서 중복 값 제거하기

    if request.user.is_authenticated:
        username = request.user
        user =get_object_or_404(get_user_model(), username=username) # 인증 확인
        user_profile = user.profile

        return render(request, 'post/post_list.html', { #인증 성공시 user_profile,post_lit,distinct_tema 보내기
            'user_profile': user_profile,
            'posts': post_list,
            'dint_tema':distinct_tema,

        })
    else:
        return render(request, 'post/post_list.html',{ #인증 성공시 post_lit,distinct_tema 보내기
            'posts': post_list,
            'dint_tema':distinct_tema,
        })

class Myprofile(ListView):
    model = Post
    template_name = 'post/myprofile.html'
    
    def dispatch(self, request, *args, **kwargs):
        username = request.user
        user =get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile
        post_list = Post.objects.all()
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('accounts:login')
        #return super(Myprofile, self).dispatch(request, *args, **kwargs)
        return render(request, 'post/myprofile.html', {
            'user_profile': user_profile,
            'posts': post_list,
        })

@login_required # 로그인 해야지만 아래 함수 실행됨
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid(): # 폼 내용이 유용하다면 
            post = form.save(commit=False) # commit=false 를 사용하여 중복 방지 하고 저장
            post.author = request.user
            post.save()
            post.tema_save()
            messages.info(request, '새 글이 등록되었습니다.')
            return redirect('post:post_list')
    else:
        form = PostForm()
    return render(request, 'post/post_new.html',{
        'form': form,
    })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('post:post_list')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid(): # 값이 있다면
            post = form.save()
            #post.tag_set.clear()
            #post.tag_save()
            messages.success(request, '수정완료')
            return redirect('post:post_list')
    
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_edit.html',{
        'post': post,
        'form': form,
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user or request.method == 'GET':
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('post:post_list')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, '삭제 완료')
        return redirect('post:post_list')

@login_required #로그인이 된상태에서만 누를수 있음
@require_POST # 포스트 방식으로만 받음
def post_like(request):
    pk = request.POST.get('pk', None) # PK값을 받음
    post = get_object_or_404(Post,pk=pk)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user) #like_set 중계모델을 사용해서 포스트와 스위치를 맺어준다.

    if not post_like_created: #like 가 만들어지지 않은 상태라면 그안에 있는것을 삭제하고 취소
        post_like.delete()
        message = "좋아요 취소"
    else: # 생성되어 있다면 좋아요 보냄
        message = "좋아요"
    
    context = {'like_count':post.like_count,
            'message':message}
    
    return HttpResponse(json.dumps(context), content_type="application/json") #json 방식으로 답을 보냄



@login_required #로그인이 된상태에서만 누를수 있음
@require_POST # 포스트 방식으로만 받음
def post_reference(request):
    pk = request.POST.get('pk', None) # PK값을 받음
    post = get_object_or_404(Post,pk=pk)
    post_reference, post_reference_created = post.reference_set.get_or_create(user=request.user) #Reference 중계모델을 사용해서 포스트와 스위치를 맺어준다.
    message = "적용해보기" #레퍼런스의 경우 누적으로 카운트가 올라가야 하기 때문에 조건문을 사용하지 않음 
    
    context = {'reference_count':post.Reference_count,
            'message':message}
    
    return HttpResponse(json.dumps(context), content_type="application/json") #json 방식으로 답을 보냄

@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return render(request, 'post/comment_new_ajax.html',{
                'comment': comment,
            })

    return redirect('post:post_list')

@login_required
def comment_delete(request):
    pk = request.POST.get('pk')
    comment = get_object_or_404(Comment,pk=pk)
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        message = '삭제완료'
        status = 1
    
    else:
        message = '잘못된 접근입니다.'
        status = 0
    return HttpResponse(json.dumps({'message':message, 'status':status, }), content_type="application/json")


