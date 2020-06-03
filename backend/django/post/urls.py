from django.urls import path
from .views import *

app_name="post"

urlpatterns=[
    path('', post_home, name="post_home"),
]