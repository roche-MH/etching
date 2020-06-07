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
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            blank=True,
                                            related_name='like_user_set',
                                            through='Like') # like_user_set 을 통해서 post.like_user_set 으로 접근이 가능하게


    reference_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            blank=True,
                                            related_name='reference_user_set',
                                            through='Reference') # like_user_set 을 통해서 post.like_user_set 으로 접근이 가능하게
            


    content = models.CharField(max_length=255, help_text="최대길이 255자 입력이 가능합니다.", blank=True) # 컨텐츠 입력
    tema = models.CharField('테마',max_length=255, help_text="테마를 입력해주세요,  #테마",blank=True) #테마 입력
    cosmetic = models.CharField('화장품',max_length=255, help_text="사용한 화장품을 입력해주세요, #제품명", blank=True) # 화장품 입력
    created_at = models.DateTimeField(auto_now_add=True) # 최초 저장시에만 현재 날짜를 적용
    updated_at = models.DateTimeField(auto_now=True) # 현재 일시 세팅

    class Meta:
        ordering = ['-created_at']

    @property # 데코레이터 힘들마ㅣㅇ너ㅣ아ㅓ
    def like_count(self):
        return self.like_user_set.count()
    
    @property
    def Reference_count(self):
        return self.reference_user_set.count()

    def __str__(self):
        return self.content

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #유저 삭제되면 라이크도 삭제
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) #생성
    updated_at = models.DateTimeField(auto_now=True) #업데이트

    class Meta:
        unique_together =(
            ('user', 'post') #유저와 포스트의 유니크한 관계를 맺어줌
        )

class Reference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #유저 삭제되면 라이크도 삭제
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) #생성
    updated_at = models.DateTimeField(auto_now=True) #업데이트
    class Meta:
        unique_together =(
            ('user', 'post') #유저와 포스트의 유니크한 관계를 맺어줌
        )

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.content