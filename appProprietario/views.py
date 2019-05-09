from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from .forms import *
from .models import *


# Create your views here.


def login_prop(request):
    name = request.POST.get('username')
    passw = request.POST.get('password')
    user = authenticate(username=name, password=passw)
    if user is not None:
        if user.is_active:
            login(request,user)
            return render(request,'index_prop.html')
        else:
            pass
    else:
        return render(request,'login_prop.html')

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
            return render(request,'index_prop.html')
        return render(request, self.template_name, {'form' : form})

