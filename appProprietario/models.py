from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from localflavor.br.br_states import STATE_CHOICES
#from wagtail.core.models import Page
#from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from django.utils.functional import cached_property
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
        return self.nome_prop

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
    prop = models.ForeignKey(Proprietario, on_delete=models.CASCADE,default="", null=True, blank=True)
    #prop_vaga = models.OneToOneField(Proprietario, on_delete=models.CASCADE,default="")
    ocupada = models.BooleanField(default=False)

    def vaga_ocupada(self):
        self.ocupada = True

    def sair_vaga(self):
        self.ocupada = False

class Cliente_Vaga(models.Model):
    cliente = models.OneToOneField(User, related_name="usuario", on_delete=models.SET_NULL,default="",null=True, editable=False)
    vaga = models.OneToOneField(Vaga, related_name="Vaga", on_delete=models.SET_NULL,default="",null=True, editable=False)