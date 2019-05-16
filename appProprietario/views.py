from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.


def login_prop(request):
    name = request.POST.get('username')
    passw = request.POST.get('password')
    cont=0
    '''if Proprietario.objects.all()==0:
        return render(request,'deu_errado.html')
    else:
        for i in Proprietario.objects.all():
            if name==i.nome_prop:
                cont+=1
    if cont>0:'''

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
        return render(request,'login_prop.html')
    '''else:
        return render(request,'deu_errado.html')'''

def logout_prop(request):
    logout(request)
    return redirect('login_prop')

@login_required
def index_prop(request):
    return render(request,'index_prop.html')

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

