from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/',login_check, name='login'),
    path('logout/', logout, name='logout'),
    path('edit/<int:pk>/',profile_edit,name='profile_edit'),
    path('follow/', follow, name='follow'),
]
