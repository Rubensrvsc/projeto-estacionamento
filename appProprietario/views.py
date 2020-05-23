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
#from django.utils import timezone
from datetime import datetime,timezone
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics,viewsets
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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import JsonResponse

from rest_auth.registration.app_settings import RegisterSerializer, register_permission_classes

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)
from rest_auth.registration.views import RegisterView


class NameRegistrationView(RegisterView):
    serializer_class = NameRegistrationSerializer



# Create your views here.
#impedir que o usuário possa entar no listapropvagas
class ClienteVagaView(APIView):

    def get(self,request,format=None):
        cliente_vaga = Cliente_Vaga.objects.all()
        cv_serializer = ClienteVagaSerializer(cliente_vaga,many=True)
        return Response(cv_serializer.data)

    def post(self,request,format=None):
        print("entrou")
        print(request.data['vaga'])
        nome_cli = request.data['cliente']
        vaga_cli_requerida = request.data['vaga']
        usuario_cliente = User.objects.get(username=nome_cli)
        vaga_requerida = Vaga.objects.get(numero_vaga=vaga_cli_requerida)
        if Cliente_Vaga.objects.filter(cliente=usuario_cliente,transacao_em_andamento=True).exists():#,vaga=vaga_requerida).exists() and Vaga.objects.filter(numero_vaga=vaga_cli_requerida,ocupada=True).exists():
            print("já existe uma vaga requerida por este cliente")
            res={"valor":"Já existe uma vaga requerida por este cliente"}
            return Response(res)
        #print("numero_vaga:{}, nome_cliente:{}".format(vaga_requerida.numero_vaga,usuario_cliente.username))
        else:
            cliente_vaga=Cliente_Vaga.objects.create(cliente=usuario_cliente,vaga=vaga_requerida,
            hora_entrada = datetime.now(),transacao_is_terminada=False)
            cli_vaga_serializer = ClienteVagaSerializer(cliente_vaga,data=request.data)
            vaga_requerida.ocupada=True
            print(vaga_requerida.ocupada)
            vaga_requerida.save()
            vcq = VagaSerializer(vaga_requerida,data=request.data)
            if vcq.is_valid() and cli_vaga_serializer.is_valid():
                vcq.save()
                cli_vaga_serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            print("numero_vaga: {}, nome_cliente: {}".format(cliente_vaga.vaga,cliente_vaga.cliente))
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def vaga_ja_alocada(request, cliente):
    usuario_cliente = User.objects.get(username=cliente)
    cliente_vaga = Cliente_Vaga.objects.filter(cliente=usuario_cliente,
        transacao_em_andamento=True)
    print("quantidade de vagas pelo cliente: "+str(cliente_vaga.count()))
    if(cliente_vaga.count()==0):
        print("não existe cliente")
        res=0
        return Response(res)
    elif(cliente_vaga.count()>0):
        print("existe vaga")
        res=1
        return Response(res)
    
    if request.method == 'GET':
        cli_vaga = ClienteVagaSerializer(cliente_vaga)
        return Response(cli_vaga.data)
    
    #return Response({"valor":"Já existe uma vaga requerida por este cliente"})

class Cria_Vaga(generics.CreateAPIView):

    queryset = Cliente_Vaga.objects.all()
    serializer_class = ClienteVagaSerializer

    def create(self,request):
        print("entrou")
        print(request.data['cliente'])
        nome_cli = request.data['cliente']
        vaga_cli_requerida = request.data['vaga']
        usuario_cliente = User.objects.get(username=nome_cli)
        vaga_requerida = Vaga.objects.get(numero_vaga=vaga_cli_requerida)
        #print("numero_vaga:{}, nome_cliente:{}".format(vaga_requerida.numero_vaga,usuario_cliente.username))
        cliente_vaga=Cliente_Vaga.objects.create(cliente=usuario_cliente,vaga=vaga_requerida)
        cli_vaga_serializer = ClienteVagaSerializer(cliente_vaga,data=request.data)
        vaga_requerida.ocupada=True
        print(vaga_requerida.ocupada)
        vaga_requerida.save()
        vcq = VagaSerializer(vaga_requerida,data=request.data)
        if vcq.is_valid() and cli_vaga_serializer.is_valid():
            vcq.save()
            cli_vaga_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        print("numero_vaga: {}, nome_cliente: {}".format(cliente_vaga.vaga,cliente_vaga.cliente))
        return Response(status=status.HTTP_404_NOT_FOUND)


class ClienteVagaSaida(generics.UpdateAPIView):

    queryset = Cliente_Vaga.objects.all()
    serializer_class = ClienteVagaSaidaSerializer

    def update(self,request):
        print(request.data)
        '''nome_cli = request.data['cliente']
        vaga_cli_requerida = request.data['vaga']

        usuario_cliente = User.objects.get(username=nome_cli)
        vaga_requerida = Vaga.objects.get(numero_vaga=vaga_cli_requerida)
        
        cv = Cliente_Vaga.objects.get(vaga=vaga_requerida)
        cv.sai_vaga()
        cv_serializer=ClienteVagaSaidaSerializer(cv,many=True)
        cv_serializer.save()
        vaga_requerida.sair_vaga()
        vaga_requerida.save()
        print("numero_vaga: {}, nome_cliente: {}".format(cv.cliente,cv.vaga))
        return Response(status=status.HTTP_200_OK)'''

class VerTodasAsVagas(APIView):

    def get(self,request):
        pass

class VerVagaRecemSaida(APIView):
    
    def get(self,request):
        cv_front = 78
        cliente_vaga = Cliente_Vaga.objects.get(id=cv_front)
        cv_serializer = ClienteVagaSaidaSerializer(cliente_vaga)
        return Response(cv_serializer.data)

class Sai_Vaga_cliente(APIView):
    def put(self,request):
        print(request.data)
        num_vaga =request.data["vaga_cliente"]
        vaga_cli = Vaga.objects.get(numero_vaga=num_vaga)
        cv = Cliente_Vaga.objects.get(vaga=vaga_cli,transacao_is_terminada=False)
        vg = cv.vaga
        vg.ocupada=False
        vg.save()
        cv.sai_vaga()
        cv_serializer=ClienteVagaSaidaSerializer(cv,data=request.data)
        vcq = VagaSerializer(vg,data=request.data)
        if vcq.is_valid() and cv_serializer.is_valid():
            vcq.save()
            cv_serializer.save()
            print("vaga saiu")
            return Response(cv_serializer.data)
        return Response(status=status.HTTP_202_ACCEPTED)

class ProcuraVagasProp(generics.ListAPIView):

    serializer_class = VagaSerializer

    def get_queryset(self):
        #print(self.kwargs)
        id_prop = self.kwargs['id']
        print(id_prop)
        vagas = Vaga.objects.filter(prop=self.kwargs['id'])
        return vagas

class VagaASerOcupada(generics.ListAPIView):

    serializer_class = VagaASerOcupadaSerializer

    def get_queryset(self):
        id_vaga = self.kwargs['vaga_id']
        print(id_vaga)
        vaga = Vaga.objects.filter(numero_vaga=id_vaga)
        return vaga

@permission_classes((IsAuthenticated,))
def exclui_vaga(request,num_vaga):
    vaga = Vaga.objects.get(numero_vaga=num_vaga)
    print(vaga.numero_vaga)
    vaga.delete()
    return redirect('index_prop')

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def obtem_vagas_prop(request,id_prop):
    try:
        vagas = Vaga.objects.filter(prop=id_prop)
    except Vaga.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        vagas_serializer = VagaSerializer(vagas, many=True)
        return Response(vagas_serializer.data)
        
@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated,))
def update_cliente_vaga_saida(request,nome_cli,id):
    #print(type(request.user.username))
    print(request.data)
    print(id)
    print(nome_cli)
    #nome_cli = request.user.username
    vaga_cli_requerida = Vaga.objects.get(numero_vaga=id)
    usuario_cliente = User.objects.get(username=nome_cli)
    print(vaga_cli_requerida.ocupada)
    print(usuario_cliente)
    print(request.data)
    vaga_cli_requerida.ocupada=False
    vaga_cli_requerida.save()
    
    try:
        user = request.user
        #cv = Cliente_Vaga.objects.get(id=id)
    except Cliente_Vaga.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        cv = Cliente_Vaga.objects.get(cliente=usuario_cliente,vaga=vaga_cli_requerida,transacao_is_terminada=False)
        cv.sai_vaga()
        cv_serializer=ClienteVagaSaidaSerializer(cv,data=request.data)
        
        vcq = VagaSerializer(vaga_cli_requerida,data=request.data)
        
        if vcq.is_valid() and cv_serializer.is_valid():
            vcq.save()
            return Response(cv_serializer.data)
    return Response(status=status.HTTP_202_ACCEPTED)

class MostraNomeProp(generics.ListAPIView):

    serializer_class = MostraNomePropsSerializer
    queryset = Proprietario.objects.all()
    permission_classes = [IsAuthenticated]


class MostraClienteVaga(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        print(request.user)
        user=User.objects.get(username=str(request.user))
        print(type(user))
        cliente_vaga = Cliente_Vaga.objects.filter(cliente=user)
        print(cliente_vaga)
        cv_serializer = MostraClienteVagaSerializer(cliente_vaga,many=True)
        return Response(cv_serializer.data)

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': request.user,  # `django.contrib.auth.User` instance.
            'auth': request.auth,  # None
        }
        return Response(request)


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
    vagas_ocupadas = []
    vagas_livres=[]
    try:
        if request.user.prop.is_prop is True:
            usuario_logado = request.user.prop
            for i in Vaga.objects.filter(ocupada=False): 
                if str(i.prop) == request.user.prop.nome_prop: 
                    vagas_livres.append(i.numero_vaga)
            for i in Vaga.objects.filter(ocupada=True): 
                if str(i.prop) == request.user.prop.nome_prop: 
                    vagas_ocupadas.append(i.numero_vaga)  
            return render(request,'index_prop.html',{'usuario_logado':usuario_logado,
            'vagas_livres':vagas_livres,'vagas_ocupadas':vagas_ocupadas})
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
            form_vaga = form.save(commit=False)
            form_vaga.prop = request.user.prop
            form_vaga.save()
            print("{} {} {}".format(form_vaga.numero_vaga,form_vaga.prop.nome_prop,form_vaga.ocupada))
            return redirect('index_prop')
        else:
            form=VagaForm()
    return render(request, 'cadastrar_vaga.html',{'form_vaga':form})


@api_view(['GET'])
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly,)) 
def obter_vagas(request):
    if request.method == 'GET':
        vagas = Vaga.objects.filter(ocupada=False)
        vagas_serializer = VagaSerializer(vagas,many=True)
        return Response(vagas_serializer.data)

@api_view(['GET'])
def obter_vagas_com_prop(request):
    pass

class VagaPropietarioGet(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Vaga.objects.all()
    serializer_class = VagaProprietarioSerializer

@api_view(['GET','POST','PUT'])
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly,)) 
def escolher_vaga(request,id_vaga):
    #vaga = Vaga.objects.filter(id=id_vaga)
    #if request.method == 'POST':
    print('entrou')
    vaga = Vaga.objects.filter(id=id_vaga)
    if vaga.ocupada == True:
        return HttpResponse('vaga já ocupada procure outra vaga')
    else:
        print(vaga)
        dados = {'cliente':request.user,'vaga':vaga}
        cv = ClienteVagaSerializer(data=dados)
        vaga.vaga_ocupada()
        if cv.is_valid():
            #vaga_serializer = VagaSerializer(vaga)
            #vaga_serializer.save()
            #Cliente_Vaga.objects.create(cliente=request.user,vaga=vaga)
            print(cv)
            cv.save()
            return Response({'valor': 'foi possivel encontrar a vaga'},status=status.HTTP_201_CREATED)
        '''else:
            return Response({'valor': 'Não foi possivel encontrar a vaga'},status=status.HTTP_400_BAD_REQUEST)
    return Response({'key': 'value'}, status=status.HTTP_200_OK)'''

def escolher_vaga_teste_entra_dados():
    pass

@api_view(['GET','PUT'])
@login_required
def sair_vaga(request,id_vaga):
    #if request.method == 'PUT':
    vaga = Vaga.objects.get(id=id_vaga)
    vaga.sair_vaga()
    vaga_serializer = VagaSerializer(data=vaga)
    #if vaga_serializer.is_valid():
    vaga.save()
    return Response({'valor': 'Vaga liberada com sucesso'},status=status.HTTP_200_OK)
    '''return Response({'valor': 'Não foi possivel encontrar a vaga'},status=status.HTTP_400_BAD_REQUEST)
    return Response({'valor': 'Não foi possivel encontrar a vaga'},status=status.HTTP_400_BAD_REQUEST)'''