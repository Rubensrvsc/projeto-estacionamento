from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from .models import * 
from .forms import ClienteForm
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView   
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from rest_framework import authentication
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from .serializers import *
from appProprietario.models import *
from appProprietario.serializers import *

# Create your views here.

'''class ExampleAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        pass

        # Get the username and password
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if not username or not password:
            raise exceptions.AuthenticationFailed(_('No credentials provided.'))

        credentials = {
            get_user_model().USERNAME_FIELD: username,
            'password': password
        }

        user = authenticate(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))


    return (user, None)'''

'''
class IndexView(View):

    template_name = 'index.html'

    def get(self,request):
        return render(request,self.template_name)'''

class RegistraClienteView(View):

    template_name = 'registrar_cliente.html'

    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        form = ClienteForm(request.POST) 
        if form.is_valid(): 
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username = dados_form['nome'], 
                                        email = dados_form['email'], 
                                        password = dados_form ['senha'])

            cliente = Cliente(nome_cliente=dados_form['nome'], 
                            idade_cliente=dados_form['idade'], 
                            email_cliente=dados_form['email'],
                            usuario_cliente=usuario)
            
            cliente.save()
            return render(request,'index.html')
        return render(request, self.template_name, {'form' : form})


@api_view(['POST'])
def registrar_cliente(request):
    if request.method == 'POST':
        form_serializer = ClienteSerializer(data=request.data) 
        if form_serializer.is_valid(): 
            #dados_form = form.cleaned_data
            '''usuario = User.objects.create_user(username = form_serializer['nome_cliente'], 
                                        email = form_serializer['email_cliente'], 
                                        password = form_serializer['senha_cliente'])'''

            form_serializer.save()
            return Response(form_serializer.data,status=status.HTTP_201_CREATED)
        return Response(form_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obter_estacionamentos(request):
    if request.method == 'GET':
        estacionamentos = Proprietario.objects.all()
        estacionamento_serializer = ProprietarioSerializer(estacionamentos,many=True)
        return Response(estacionamento_serializer.data)





