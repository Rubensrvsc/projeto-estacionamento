from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=255)
    idade_cliente = models.IntegerField()
    email_cliente = models.EmailField()
    senha_cliente = models.CharField(max_length=30)
    #usuario_cliente = models.OneToOneField(User, related_name="Cliente", on_delete = models.CASCADE,default="", editable=False)
