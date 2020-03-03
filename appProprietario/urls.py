from django.contrib import admin
from django.urls import include,path
from .views import *
from rest_framework import routers
from django.views.generic.base import TemplateView
from django.contrib.auth import login,views
from django.conf.urls import url
from .forms import *

urlpatterns =[
    #path('login_prop/', login_prop,name='login_prop'),
    #path('logout_prop/',logout_prop,name='logout_prop'),
    path('index_prop/',index_prop,name='index_prop'),
    path('registra_prop/',PropView.as_view(),name='registra_prop'),
    #path('rest-auth/registrar/', RegisterViewCliente.as_view()),
    #path('login_cliente/',LoginViewCliente.as_view(),name='login_cliente'),
    #path('logout_cliente/',LogoutView.as_view(),name='logout_cliente'),
    path('registra_cliente/',RegisterClienteView.as_view(),name='registra_cliente'),
    #path('rest-auth/', include('rest_auth.urls')),
    #path('clientevaga/',ClienteVagaView.as_view(),name='clientevaga'),
    path('clientevagacreate/',ClienteVagaCreate.as_view(),name='clientevagacreate'),
    #path('clientevagasaida/<int:id>/',ClienteVagaSaida.as_view(),name='clientevagasaida'),
    path('clientesaidavaga/<str:nome_cli>/<int:id>/',update_cliente_vaga_saida,name='update_vaga'),
    #path('', include(router.urls)),
    path('mostraclientevaga/',MostraClienteVaga.as_view(),name='mostraclientevaga'),
    path('saidavaga/',ClienteVagaSaida.as_view(),name='saidavaga'),
    path('cadastrar_vaga/',cadastrar_vaga,name='cadastrar_vaga'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name = "login"), 
    path('logout/', views.LogoutView.as_view(template_name='login.html'), name="logout"),
    path('obter_vagas/',obter_vagas,name="obter_vagas"),
    path('escolher_vaga/<int:id_vaga>',escolher_vaga,name='escolher_vaga'),
    path('sair_vaga/<int:id_vaga>',sair_vaga,name='sair_vaga'),
    path('vervagas/', VagaPropietarioGet.as_view(), name = "vervagas"), 

]