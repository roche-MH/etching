from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('accounts/',include('allauth.urls')),
    path('post/',include('post.urls',namespace='post')),
    path('', lambda r: redirect('post:post_home'), name='root'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 세팅스에 설정했던 스택틱 관련 내용을 불러오는것
