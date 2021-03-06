from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists,
                               get_username_max_length)
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_auth.models import TokenModel

class NameRegistrationSerializer(RegisterSerializer):
    
    escolha=(
        ('n','Normal'),
        ('i','Idoso'),
        ('g','gestante'),
        ('d','deficiente')
    )

    
    #escolhe_tipo = serializers.ChoiceField(required=False,choices=escolha,allow_blank=True)
    first_name = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        #user.escolhe_tipo = self.validated_data.get('escolhe_tipo','')
        user.save(update_fields=['first_name'])


class ProprietarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proprietario
        fields = '__all__'

class VagaProprietarioSerializer(serializers.ModelSerializer):
    
    prop_vaga = serializers.ReadOnlyField(source='prop.nome_prop')
    
    class Meta:
        model = Vaga
        fields = ('numero_vaga','prop_vaga','ocupada')

class VagaASerOcupadaSerializer(serializers.ModelSerializer):

    prop_vaga = serializers.ReadOnlyField(source='prop.nome_prop')

    class Meta:
        model = Vaga
        fields = '__all__'

class VagaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vaga
        fields = '__all__'

class ClienteVagaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente_Vaga
        fields = ('cliente','vaga',)

class ClienteVagaSaidaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente_Vaga
        fields = '__all__'

class ClienteVagaJsonSerializer(serializers.ModelSerializer):

    num_vaga = serializers.ReadOnlyField(source='vaga.numero_vaga')
    vaga_ocupada = serializers.ReadOnlyField(source='vaga.ocupada')
    tipo_vaga = serializers.ReadOnlyField(source='vaga.tipo_vaga')

    class Meta:
        model = Cliente_Vaga
        fields = ('vaga','cliente','hora_entrada',
        'transacao_is_terminada','transacao_em_andamento','num_vaga','vaga_ocupada',
        'tipo_vaga')

class MostraNomePropsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proprietario
        fields = ('nome_prop','id')

class MostraClienteVagaSerializer(serializers.ModelSerializer):

    num_vaga = serializers.ReadOnlyField(source='vaga.numero_vaga')

    class Meta:
        model = Cliente_Vaga
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = ('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = ('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = ('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = ('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = ('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs

class RegisterSerializerCliente(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
