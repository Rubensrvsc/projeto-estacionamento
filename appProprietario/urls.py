from django.contrib import admin
from django.urls import include,path
from .views import *

urlpatterns =[
    path('add_proprietario/',index,name='index_proprietario'),
]