from django.contrib.auth import get_user_model #유저모델 가져오기
from django.shortcuts import get_object_or_404, render # 404 render 기능 불러오기
from .models import Post #Post 모델 가져오기

def post_home(request):

    post_home = Post.objects.all()

    if request.user.is_authenticated:
        username = request.user
        user = get_object_or_404(get_user_model(), username=username) #인증 확인
        user_profile = user.profile

        return render(request, 'post/post_home.html', {
            'user_profile': user_profile,
            'posts': post_home,
        })
    else:
        return render(request, 'post/post_home.html', {
            'posts': post_home,
        })