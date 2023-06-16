from django.contrib import admin

from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', UserInfo, name='UserInfo'),
    path('edit',  EditUserInfo, name='Edituserinfo'),
    path('edit', EditUser, name='EditUser'),
    path('deleteasdasdasdsad', deleteuser, name='deleteuser'),
    
]