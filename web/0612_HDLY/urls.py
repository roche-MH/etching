from django.urls import path
from .views import *

app_name="post"

urlpatterns=[
    path('', post_list, name="post_list"),
    path('profile', Myprofile.as_view(), name='post_profile'),
    path('new', post_new, name='post_new'),
    path('edit/<int:pk>/',post_edit,name='post_edit'),
    path('delete/<int:pk>/',post_delete,name='post_delete'),
    path('<int:pk>/', post_detail, name='post_detail'),
    path('profile/<int:pk>/', post_profile_pk, name='post_profile_pk'),

    path('like',post_like,name='post_like'),
    path('reference', post_reference, name='post_reference'),

    path('comment/new',comment_new, name='comment_new'),
    path('comment/delete',comment_delete, name='comment_delete'),
    path('explore/temas/<tema>/', post_detail, name="post_find"),

    # 인풋 urls
    path('imginput/',image_input, name='image_input'),
    path('imginput/imgprocess',image_process, name='image_process'),
    path('imgoutput',image_output, name='image_output'),

    # addtional functions urls
    path('faceratio/', face_ratio, name='face_ratio'),
    path('personalcolor/', personal_color, name='personal_color'),
]