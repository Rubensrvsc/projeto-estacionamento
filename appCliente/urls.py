from django.contrib import admin
from django.urls import include,path
from .views import *
from django.contrib.auth import views as v
from .views import *

urlpatterns =[
    #path('login_cliente/', v.LoginView.as_view(template_name='login_cliente.html'), name = 'login'), 
    #path('logout_usuario/', v.LogoutView.as_view(template_name='login_cliente.html'), name="logout"),
    path('registrar_cliente/',registrar_cliente,name='registrar_cliente'),
    path('obter_estacionamentos/',obter_estacionamentos,name='obter_estacionamentos'),
    #path('index_cliente/',IndexView.as_view(),name='index_cliente'),
    #path('login_cliente/', include('rest_framework.urls')),
]