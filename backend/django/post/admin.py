from django import forms
from django.contrib import admin
from .models import Post, Like, Reference, Comment

class PostForm(forms.ModelForm): #컨테스트창 크기 늘려주기
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = '__all__'

class LikeInline(admin.TabularInline):
    model = Like # 표형식으로 어드민 페이지 정리됨

class CommentInline(admin.TabularInline):
    model = Comment # 표형식으로 어드민 페이지 정리됨


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','author','nickname','content','created_at']
    list_display_links = ['author','nickname','content']
    form = PostForm
    inline = [LikeInline, CommentInline]

    def nickname(request, post):
        return post.author.profile.nickname

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display=['id','post','user','created_at']
    list_display_links = ['post', 'user'] #클릭했을때 링크가 달리는 부분


@admin.register(Reference)
class RederenceAdmin(admin.ModelAdmin):
    list_display=['id','post','user','created_at']
    list_display_links = ['post', 'user'] #클릭했을때 링크가 달리는 부분


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['post','content','author','created_at']
    list_display_links = ['post','content','author'] #클릭했을때 링크가 달리는 부분
