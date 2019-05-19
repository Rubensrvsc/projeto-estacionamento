from rest_framework import serializers
from .models import *

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:

        model = Cliente
        fields = ('nome_cliente','idade_cliente','email_cliente','senha_cliente',)