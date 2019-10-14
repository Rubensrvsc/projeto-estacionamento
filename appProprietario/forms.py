from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class PropForm(forms.Form): 
    nome_prop = forms.CharField(required=True) 
    email_prop = forms.EmailField(required=True) 
    senha_prop = forms.CharField(required=True) 


    def is_valid(self): 
        valid = True 
        if not super(PropForm, self).is_valid(): 
            self.adiciona_erro('Por favor, verifique os dados informados')
            user_exists = User.objects.filter(username=self.cleaned_data['nome_prop']).exists()
            valid = False 
            if user_exists: 
                self.adiciona_erro('Usuário já existente.')  
                valid = False
        return valid
    def adiciona_erro(self, message): 
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList()) 
        errors.append(message)

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = '__all__'

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))