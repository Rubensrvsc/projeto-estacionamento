from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Proprietario(models.Model):
    nome_prop = models.CharField(max_length=255)
    email_prop = models.EmailField()
    usuario_prop = models.OneToOneField(User, related_name="Propietario", on_delete = models.CASCADE,default="", editable=False)
    

class Vaga(models.Model):
    numero_vaga = models.IntegerField()
    prop = models.ForeignKey(Proprietario, on_delete=models.CASCADE)