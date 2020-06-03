from django.contrib import admin
from .models import Profile ##Model 에서 정의한 Profile class 를 불러온다.
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'user'] #id는 장고에서 자동으로 지원, 뭘볼건지 지정
    list_display_links = ['nickname','user']
    search_fields = ['nickname']