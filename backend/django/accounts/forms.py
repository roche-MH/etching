from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from django.contrib.auth.models import User # DB 에서 USER 내용을 불러온다.

class LoginForm(forms.ModelForm):
    class Meta: # 아래로 넘긴다.
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