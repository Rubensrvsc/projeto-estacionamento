from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from .forms import *
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from rest_auth.models import TokenModel
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .permissions import IsOwnerOrReadOnly

from rest_auth.registration.app_settings import RegisterSerializer, register_permission_classes

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)

# Create your views here.


'''def login_prop(request):
    name = request.POST.get('username')
    passw = request.POST.get('password')
    cont=0
    if Proprietario.objects.all()==0:
        return render(request,'deu_errado.html')
    else:
        for i in Proprietario.objects.all():
            if name==i.nome_prop:
                cont+=1
    if cont>0:

    user = authenticate(username=name, password=passw)
    if user is not None:
        for i in Proprietario.objects.all():
            if name==i.nome_prop:
                cont+=1
        if cont==0:
            return render(request,'deu_errado.html')
        if user.is_active:
            login(request,user)
            return render(request,'index_prop.html')
        else:
            pass
    else:
        return redirect('index_prop')
    else:
        return render(request,'deu_errado.html')
@login_required
def logout_prop(request):
    logout(request)
    return redirect('login_prop')'''

@login_required
def index_prop(request):
    usuario_logado = request.user
    return render(request,'index_prop.html',{'usuario_logado':usuario_logado})

class PropView(View):

    template_name = 'registrar_proprietario.html'

    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        form = PropForm(request.POST) 

        if form.is_valid(): 
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username = dados_form['nome_prop'], 
                                        email = dados_form['email_prop'], 
                                        password = dados_form['senha_prop'])

            prop = Proprietario(nome_prop=dados_form['nome_prop'],  
                            email_prop=dados_form['email_prop'],
                            usuario_prop=usuario)
            
            prop.save()
            return redirect('index_prop')
        return render(request, self.template_name, {'form' : form})

class RegisterViewCliente(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterViewCliente, self).dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        content = {
            "details": "Registered"
        }
        return Response(content,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)

        complete_signup(self.request._request, user, None, None)
        return user

#@login_required
def cadastrar_vaga(request):
    form=VagaForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('index_prop')
        else:
            form=VagaForm()
    return render(request, 'cadastrar_vaga.html',{'form':form})


@api_view(['GET'])
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly,)) 
def obter_vagas(request):
    pass

@api_view(['POST','PUT'])
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly,)) 
def escolher_vaga(request):
    pass
