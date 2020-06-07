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

    path('like',post_like,name='post_like'),
    path('reference', post_reference, name='post_reference'),

    path('comment/new',comment_new, name='comment_new'),
    path('comment/delete',comment_delete, name='comment_delete'),
    
]