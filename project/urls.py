from django.urls import path
from .views import *


urlpatterns = [
    
    path('create', createProject,name='createProject'),
    path('all', listAllProject,name='allprojects'),
    path('display/<int:id>', displayProject,name='displayProject'),
    path('delete/<int:ID>', deleteProject,name='deleteProject'),
    
    
]