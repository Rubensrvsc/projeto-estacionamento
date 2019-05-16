from django.contrib import admin
from django.urls import include,path
from .views import *
from django.views.generic.base import TemplateView
from django.contrib.auth import login
from django.conf.urls import url
from .forms import *

urlpatterns =[
    path('login_prop/', login_prop,name='login_prop'),
    path('logout_prop',logout_prop,name='logout_prop'),
    path('index_prop',index_prop,name='index_prop'),
    path('registra_prop/',PropView.as_view(),name='registra_prop')
]