from django.db import models
from django.contrib.auth.models import User
#from geoposition.fields import GeopositionField
#from localflavor.br.br_states import STATE_CHOICES
#from wagtail.core.models import Page
#from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from django.utils.functional import cached_property
from datetime import datetime
from django.utils import timezone
#from wagtailgeowidget.edit_handlers import GeoPanel


# Create your models here.

class Proprietario(models.Model):

    nome_prop = models.CharField(max_length=255)
    email_prop = models.EmailField()
    #nome_loc_prop = models.CharField(max_length=250, blank=True, null=True)
    is_prop = models.BooleanField(default=True)
    #tipo_prop=models.CharField(choices=prop_choices)
    usuario_prop = models.OneToOneField(User, related_name="prop", on_delete=models.CASCADE,editable=False)
    #position = GeopositionField(verbose_name=u'Geolocalização', help_text="Não altere os valores calculados automaticamente de latitude e longitude")
    
    def __str__(self):
        return '{}'.format(self.nome_prop)

    '''content_panels = Page.content_panels + [
        GeoPanel('location'),
    ]

    class Meta:
        verbose_name, verbose_name_plural = u"Sua Classe" , u"Suas Classes"
        ordering = ('usuario_prop',)

    def __unicode__(self):
        return u"%s" % self.endereco 

    @cached_property
    def point(self):
        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point['y']

    @property
    def lng(self):
        return self.point['x']'''

class Cliente(models.Model):
    nome_cli = models.CharField(max_length=255)
    email_cli = models.EmailField()
    is_cliente = models.BooleanField(default=True)
    #usuario_cli = models.OneToOneField(User, related_name="Cliente", on_delete=models.SET_NULL,default="",null=True, editable=False)
    usuario_cli = models.OneToOneField(User, related_name="Cliente", on_delete=models.CASCADE, editable=False)

class Vaga(models.Model):
    numero_vaga = models.IntegerField()
    prop = models.ForeignKey(Proprietario,related_name="prop_vaga", on_delete=models.CASCADE,default="", null=True, blank=True)
    #prop_vaga = models.OneToOneField(Proprietario, on_delete=models.CASCADE,default="")
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.numero_vaga)

    def vaga_ocupada(self):
        self.ocupada = True

    def sair_vaga(self):
        self.ocupada = False

    def natural_key(self):
        return (self.numero_vaga,) + self.prop.natural_key()
    natural_key.dependencies = ['appProprietario.models.Proprietario']

class Cliente_Vaga(models.Model):
    cliente = models.ForeignKey(User, related_name="usuario", on_delete=models.SET_NULL,default="",null=True, editable=False)
    vaga = models.ForeignKey(Vaga, related_name="Vaga", on_delete=models.SET_NULL,default="",null=True, editable=False)
    #horário de entrada
    hora_entrada = models.DateTimeField(default=timezone.now(), blank=True)
    #horário de saída
    hora_saida = models.DateTimeField(null=True)
    #total em dinheiro
    total_transacao = models.FloatField(null=True)
    #transação terminada ou não
    transacao_is_terminada = models.BooleanField(default=False)

    def sai_vaga(self):
        self.hora_saida=timezone.now()
        diff = self.hora_saida.minute - self.hora_entrada.minute
        tempo = diff
        self.total_transacao = tempo * 0.1
        self.transacao_is_terminada = True
        self.save()

