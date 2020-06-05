pip install django==2.1



django-admin startproject config .

현재 경로에 설치 (config에 중요파일을 넣는다.)



python manage.py migrate (데이터베이스를 연동)

settings.py -> ALLOWED_HOSTS = ['*']



# Accounts

## create,settings

1. django-admin startapp accounts

2. config 폴더안에 templates , static 추가 

3. static 폴더안에 css,js 폴더 추가

4. settings.py 설정 

```python
INSTALLED_APPS = [
    'accounts',
```

```python
Template
'DIRS': [
            os.path.join(BASE_DIR,'config','templates'),
        ],
```

```python
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'
```

```python
STATICFILES_DIRS = [ ## 마지막줄 추가
    os.path.join(BASE_DIR, 'config', 'static',)
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'
```



## accounts modle

```python
pip install pillow
pip install pilkit
pip install psycopg2-binary
pip install django-imagekit
```

```python
# accounts/models.py
from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField # 이미지 처리
from imagekit.processors import ResizeToFill #이미지 원하는 사이지로 처리해줌
# Create your models here.

def user_path(instance, filename):  #포토모델, 사용자가 업로드한 파일이름
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)] #대소문자 구분 x
    pid = ''.join(arr)
    extension = filename.split('.')[-1] #확장자
    return 'accounts/{}/{}.{}'.format(instance.user.username, pid, extension)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #(계정)django 에서 관리하는 유저 라이브러리
    nickname = models.CharField('별명',max_length=20, unique=True) # (닉네임)
    picture = ProcessedImageField(upload_to=user_path,processors=[ResizeToFill(150,150)],format='JPEG',options={'quality':90},blank=True) #업로드 사이즈 지정
    about = models.CharField(max_length=255, blank=True) #(소개글)blank 비워도 된다.

    skinton_Cho = ( #(피부톤선택)
        ('선택안함', '선택안함'),
        ('쿨톤','쿨톤'),
        ('웜톤','웜톤'),
    )    
    skinton = models.CharField('피부톤',max_length=10,choices=skinton_Cho, default='N') #(피부톤선택)

    GENDER_Cho = (       #(성별선택)
        ('선택안함', '선택안함'),
        ('여성','여성'),
        ('남성','남성'),
    )
    gender = models.CharField('성별(선택사항)', max_length=10,choices=GENDER_Cho, default='N') #(성별선택)

    def __str__(self):
        return self.nickname #닉네임 대표로
```

python manage.py makemigrations accounts

python manage.py migrate ## DB 적용



## accounts admin

accounts/admin.py

```python
from django.contrib import admin
from .models import Profile ##Model 에서 정의한 Profile class 를 불러온다.
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'user'] #id는 장고에서 자동으로 지원, 뭘볼건지 지정
    list_display_links = ['nickname','user'] # 링크는 닉네임,유저
    search_fields = ['nickname','skinton'] # 서치기능 닉네임,스킨톤
```

```python
python manage.py createsuperuser

```

admin 페이지에 접속하면 accounts > Profiles 라고 만들어져 있고, 추가를 눌렀을때 models 에서 만든 class profile 의 내용이 들어가 있다.



내용을 추가하면 accounts/media/사용자계정명/난수.jpeg 로 저장됨 사이즈는 (150,150)



## 프론트앤드 파트 파일 확인

css, images, js 는 static 으로 넣는다.

html 파일은 templates 로 넣어준다.



## templates : layout

기본적으로 모든 페이지에 들어가는 헤드 부분이라던지 바텀 부분등을 html 마다 만들어주지 않고 layout.html 또는 base.html 이라고 만들어서 불필요한 과정을 없앤다.

template/layout 폴더를 만들고 그안에 layout.html 을 만든다.

아래 코드는 우리가 사용할 탑 네비게이션과 바텀 네비게이션이고

{% load static %} 은 static 폴더를 정의하고

{% block content %}, {% endblock %} 이 두개를 사용해서 페이지별 내용이 들어갈 부분을 지정해준다. 두개 사이의 값은 페이지별 변경가능

```python
{% load static %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="{% static 'css/search.css'%}">
    <link rel="stylesheet" href="{% static 'css/layout.css'%}">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
</head>
<body>
    <body>
   
        <div class="main-container">
       
        <div class="nav-top">
        
         <ul>
         
          <li class="nav-start"><a><i class="fas fa-camera" style="color:black;"></i></a></li>
          
          <li class="nav-img"><a><img src="{% static 'images/icon/title_img.png'"/></a></li>
          
          <li class="nav-end"><a><i class="fas fa-location-arrow" style="color:black;"></i></a></li>
         
         </ul>
         
        </div>
        {% block content %}
        <div id="Home" class="container actives">
            
           <p>Home</p>	  
            
        </div>
        
        <div id="Search" class="container">
         
             <p>Search</p>
             
         </div>
        
        <div id="Upload" class="container">
              
               <p>Upload</p>	
               
        </div>
        
        <div id="Users" class="container">
            
             <p>Users</p>	
             
        </div>
        
        <div id="Profile" class="container">
            
             <p>Profile</p>	
        </div>
        
        {% endblock %}
        <div class="nav-bottom">
        
          <ul>
            <li><a class="tab active"  href="./index.html"><i class="fas fa-home"></i></a></li>
            
           <li><a class="tab"  href="./search/search.html"><i class="fas fa-search"></i></a></li>
           
           <li> <a class="tab" href="./input_img_page/input_page.html" > <i class="fas fa-plus"></i></a></li>
           
           <li><a class="tab" href="Users"><i class="fas fa-heart"></i></a></li>
           
           <li><a class="tab" href="./profile/mypage_1.html"><i class="fas fa-user"></i></a></li>
         
          
          </ul>
        
        </div>
        
       
       </div>

</body>
</html>
```



## 회원가입, 로그인, 로그아웃

```python
pip install django-allauth #계정에 필요한 라이브러리 소셜로그인을 쓰기위해서도 필요함
```

settings.py

```pyhton
INSTALLED_APPS = [
    'django.contrib.sites',
    'allauth',
    'allauth.account', #추가
]
SITE_ID =1
```



config/urls.py

```python
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

# url 기본 작동은 사용자가 url에서 입력한 값을 뒤 인자로 보내주는 것
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('accounts/',include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 세팅스에 설정했던 스택틱 관련 내용을 불러오는것

```

accounts로 들어온 사용자를 안내하기위해 urls.py 를 만들어준다.

```python
from django.urls import path
from .views import * #views 파일의 내용들 전부 불러오고

app_name = 'accounts' #이름지정

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/',login_check, name='login'),
    path('logout/', logout, name='logout'),
]
```



### Views 정의

views.py 는 사용자가 접근했을때 어떻게 동작해라 라고 정의해주는것

accounts/views.py

```python
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
```

accounts/forms.py

```python
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from django.contrib.auth.models import User # DB 에서 USER 내용을 불러온다.

class LoginForm(forms.ModelForm):
    class Meta:
        model = User # model 입력
        fields = ["username","password"] # 유저명과 패스워드 가져온다.

class SignupForm(UserCreationForm):
    username = forms.CharField(label="사용자명", widget=forms.TextInput(attrs={
        'pattern': '[a-zA-Z0-9]+',
        'title': '특수문자, 공백 입력불가',
    }))

    nickname = forms.CharField(label='닉네임')
    picture = forms.ImageField(label='프로필 사진', required=False)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_nickname(self): # 유효성 검사
        nickname = self.cleaned_data.get('nickname') 
        if Profile.objects.filter(nickname=nickname).exists(): # 닉네임 중복이 있는지 없는지
            raise forms.ValidationError('중복되는 닉네임 입니다.')
        return nickname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model() # 유저데이터 가져와서
        if User.objects.filter(email=email).exists(): # 있는지 확인
            raise forms.ValidationError('사용중인 이메일 입니다.')
        return email
    
    def clean_picture(self): # 입력된 사진이 없다면 픽쳐 없다고 나타내기
        picture = self.cleaned_data.get('picture')
        if not picture:
            picture = None
        return picture

    def save(self): # 저장
        user = super().save()
        Profile.objects.create(
            user=user,
            nickname=self.cleaned_data['nickname'],
            picture=self.cleaned_data['picture'],
        )
        return user
```

Class Meta는 필수적으로 입력해야되는 옵션 값이 아닌 모델단위 옵션을 넣어주고 싶을때 입력하는 값, 필드 단위에서 옵션을 주고 싶을때는 nickname = forms.CharField(lable='닉네임') 이렇게 지정한다.

대충 class Meta는 모델단위의 옵션을 주고 싶을때 사용한다고 생각하면 된다.

https://docs.djangoproject.com/en/2.2/ref/models/options/ <- 여기 더 있음





### login.html, signup.html 을 만들어서 넣어줌



## 메인 화면 create,settings,model

django-admin startapp post

settings.py installapp 에 post 를 추가해준다.

이후 post > models.py 에 들어가서 model를 정립해준다.

```python
from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField # 이미지 불러오기
from imagekit.processors import ResizeToFill # 사이즈 조절

def photo_path(instance, filename):
    from time import strftime
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)] # 난수 8글자 랜덤으로 지정
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return '{}/{}/{}.{}'.format(strftime('post/%Y/%m/%d/'), instance.author.username, pid, extension) # 업로드 파일 저장 위치

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = ProcessedImageField(upload_to=photo_path,
                                processors=[ResizeToFill(600,600)], ## 이미지 사이즈 600, 600
                                format = 'JPEG',  # 파일 확장자 JPEG
                                options={'qualty':90})
    
    content = models.CharField(max_length=255, help_text="최대길이 255자 입력이 가능합니다.", blank=True) # 컨텐츠 입력
    tema = models.CharField('테마',max_length=255, help_text="테마를 입력해주세요,  #테마",blank=True) #테마 입력
    cosmetic = models.CharField('화장품',max_length=255, help_text="사용한 화장품을 입력해주세요, #제품명", blank=True) # 화장품 입력
    created_at = models.DateTimeField(auto_now_add=True) # 최초 저장시에만 현재 날짜를 적용
    updated_at = models.DateTimeField(auto_now=True) # 현재 일시 세팅

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
```

python manage.py makemagrations post

python manage.py migrate

post/admin.py

```python
from django import forms
from django.contrib import admin
from .models import Post

class PostForm(forms.ModelForm): #컨테스트창 크기 늘려주기
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','author','nickname','content','created_at']
    list_display_links = ['author','nickname','content']
    form = PostForm

    def nickname(request, post):
        return post.author.profile.nickname #닉네임은 post 에 없으니까 함수로 만들어줘야한다.
```



## 메인화면 : url, views

config urls.py 에 post 로 들어오는것 추가

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('accounts/',include('allauth.urls')),
    path('post/',include('post.urls',namespace='post')),
    path('', lambda r: redirect('post:post_home'), name='root'), ## root로 들어왔을때 post_home 으로 보내도록 설정
]
```

이후 post 파일에 urls.py 를 만들어서 내용 추가

```python
from django.urls import path
from .views import *

app_name="post"

urlpatterns=[
    path('', post_home, name="post_home"),
]
```

Post/views.py

```python
from django.contrib.auth import get_user_model #유저모델 가져오기
from django.shortcuts import get_object_or_404, render # 404 render 기능 불러오기
from .models import Post #Post 모델 가져오기

def post_list(request):

    post_list = Post.objects.all() # model 객체 불러오기
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
```



