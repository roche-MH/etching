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
        return post.author.profile.nickname