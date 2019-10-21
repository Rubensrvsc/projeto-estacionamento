from django.shortcuts import render,redirect
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout
)
from django.views.generic.base import View
from .forms import *
from .models import *
from django.conf import settings
from .serializers import *
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from rest_auth.models import TokenModel
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .permissions import IsOwnerOrReadOnly
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

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
    try:
        if request.user.prop.is_prop is True:
            return render(request,'index_prop.html')
    except ObjectDoesNotExist:
        return redirect('logout')

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
            print(prop.nome_prop)
            print(prop.email_prop)
            print(prop.is_prop)
            print(usuario.prop.nome_prop)
            
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

class LoginViewCliente(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginViewCliente, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    '''def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer'''

    def login(self):
        self.user = self.serializer.validated_data['user']

        '''if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)'''

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        '''serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)'''
        return HttpResponse("deu certo")

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()

class LogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.logout(request)
        #request.session.flush()
        #return redirect('login_cliente/')

    def logout(self, request):
        try:
            request.user.auth_token.delete()
            #token = Token.objects.get_or_create(user=request.user)
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": ("Successfully logged out.")},
                            status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
        return response

class RegisterClienteView(CreateAPIView):
    serializer_class = RegisterSerializerCliente
    permission_classes = register_permission_classes()
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterClienteView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": ("Verification e-mail sent.")}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            return JWTSerializer(data).data
        else:
            return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        '''if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)'''

        complete_signup(self.request._request, user,
                        allauth_settings.EMAIL_VERIFICATION,
                        None)
        return user

@login_required
def cadastrar_vaga(request):
    form=VagaForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save(commit=False)
            form.prop = request.user.prop
            return redirect('index_prop')
        else:
            form=VagaForm()
    return render(request, 'cadastrar_vaga.html',{'form':form})


@api_view(['GET'])
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly,)) 
def obter_vagas(request):
    if request.method == 'GET':
        vagas = Vaga.objects.filter(ocupada=False)
        vagas_serializer = VagaSerializer(vagas,many=True)
        return Response(vagas_serializer.data)

@api_view(['POST','PUT'])
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly,)) 
def escolher_vaga(request):
    pass
