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
    follow_set = models.ManyToManyField('self', blank=True,through='Follow', symmetrical=False) #비대칭 관계 적용 symmtrical
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

    @property
    def get_follower(self):
        return [i.from_user for i in self.follower_user.all()] #나를 팔로워한 유저를 확인
    
    @property
    def get_following(self):
        return [i.to_user for i in self.follow_user.all()] #내가 팔로워한 유저를 확인
    
    @property
    def follower_count(self):
        return len(self.get_follower)
    
    @property
    def following_count(self):
        return len(self.get_following)

    def is_follower(self, user):
        return user in self.get_follower # 만약 팔로우한 사람 누군지 폴려면 필요함

    def is_following(self, user):
        return user in self.get_following


class Follow(models.Model):
    from_user = models.ForeignKey(Profile, #셀프 참조?? 
                                related_name='follow_user', #팔로잉사용자 체크할때 필요
                                on_delete=models.CASCADE)
    
    to_user = models.ForeignKey(Profile,related_name='follower_user',
                                on_delete=models.CASCADE)
        
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} -> {}".format(self.from_user, self.to_user)

    class Meta:
        unique_together =(
            ('from_user','to_user') # 두 관계가 중복없이 유니크하게 관계를 맺을수 있도록 해줌
        )
