from rest_framework import serializers
from .models import *

class ProprietarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proprietario
        fields = ('nome_prop','email_prop',)