from django.contrib import admin
from django.urls import include,path
from .views import *
from django.views.generic.base import TemplateView
from django.contrib.auth import login,views
from django.conf.urls import url

urlpatterns =[
    path('testeserializer/', TesteSerializer.as_view(), name = "testeserializer"), 
    path('category/', CategorySerializerCreate.as_view(), name = "category"), 
    path('item/', ItemSerializerCreate.as_view(), name = "item"), 
    path('category/<int:id>/',ProcuraCategory.as_view(),name='procura'),
    path('item/<int:id_item>/',ProcuraItemView.as_view(),name='procura_item')

]
