from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm): # 모델에서 폼 불러오기
    content =forms.CharField(label='',widget=forms.Textarea(attrs={ #html 짜기
        'class': 'post-new-content',
        'rows': 5,
        'cols': 50,
        'placeholder': '255자 까지 등록 가능합니다.'
    }))
    tema = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'테마를 입력해주세요'}))
    cosmetic = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'사용한 화장품을 입력해주세요'}))

    class Meta:
        model = Post
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
