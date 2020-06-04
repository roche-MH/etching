from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField # 이미지 불러오기
from imagekit.processors import ResizeToFill # 사이즈 조절

def photo_path(instance, filename):
    from time import strftime
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return '{}/{}/{}.{}'.format(strftime('post/%Y/%m/%d/'), instance.author.username, pid, extension)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = ProcessedImageField(upload_to=photo_path,
                                processors=[ResizeToFill(600,600)],
                                format = 'JPEG',
                                options={'qualty':90})
    
    content = models.CharField(max_length=255, help_text="최대길이 255자 입력이 가능합니다.")
    tema = models.CharField('테마',max_length=255, help_text="테마를 입력해주세요,  #테마")
    cosmetic = models.CharField('화장품',max_length=255, help_text="사용한 화장품을 입력해주세요, #제품명")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content