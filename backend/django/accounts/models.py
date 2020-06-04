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