from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from .models import * 
from .forms import ClienteForm
from django.db import IntegrityError, transaction
from django.http import HttpResponse

# Create your views here.

class IndexView(View):

    template_name = 'index.html'

    def get(self,request):
        return render(request,self.template_name)

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



