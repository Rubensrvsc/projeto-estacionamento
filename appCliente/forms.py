from .models import *
from django import forms
from django.contrib.auth.models import User


class ClienteForm(forms.Form): 
    nome = forms.CharField(required=True) 
    email = forms.EmailField(required=True) 
    senha = forms.CharField(required=True) 
    idade = forms.IntegerField(required=True) 

    def is_valid(self): 
        valid = True 
        if not super(ClienteForm, self).is_valid(): 
            self.adiciona_erro('Por favor, verifique os dados informados')
            user_exists = User.objects.filter(username=self.cleaned_data['nome']).exists()
            valid = False 
            if user_exists: 
                self.adiciona_erro('Usuário já existente.')  
                valid = False
        return valid
    def adiciona_erro(self, message): 
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList()) 
        errors.append(message)
