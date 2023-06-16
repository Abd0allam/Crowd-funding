from django.urls import path
from .views import *


urlpatterns = [
    
    path('', myHome,name='myHome'),
    path('category/<str:cate>', getCategory,name='category'),
    path('Registeration',Registeration,name='Registeration'),
    path('Login',Login,name='Login'),
    path('Logout',Logout,name='Logout'),
    
]