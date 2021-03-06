from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm): # 모델에서 폼 불러오기
    #photo = forms.ImageField(label='', required=False) #중복 표현 x

    content = forms.CharField(label='글쓰기', widget=forms.Textarea(attrs = { #html 짜기
        'class': 'post-new-content',
        'rows': 5,
        'cols': 50,
        'placeholder': '255자 까지 등록 가능합니다.'
    }))

    # HashTag -- 입력 방식 수정해주세요 대표님
    tema = forms.CharField(label='테  마', widget=forms.TextInput(attrs = {
        'width' : 50,
        'placeholder':'테마를 입력해주세요'
    }))

    cosmetic = forms.CharField(label='화장품', widget=forms.TextInput(attrs = {
        'width' : 50,
        'placeholder':'사용한 화장품을 입력해주세요'
    }))

    class Meta:
        model = Post
        # fields = ['photo', 'content','tema','cosmetic']
        fields = ['content','tema','cosmetic']

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'comment-form',
        'size': '70px',
        'placeholder': '댓글 달기...',
        'maxlength': '80',
    }))
    class Meta:
        model = Comment
        fields = ['content']