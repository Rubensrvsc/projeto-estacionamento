"""ProjetoEstacionamento URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path, re_path
from appCliente.views import *
from appProprietario.views import *
from rest_framework_jwt.views import refresh_jwt_token
from rest_auth.registration.views import VerifyEmailView, RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('auth/refresh-token/', refresh_jwt_token),
    #path('auth/signup/',NameRegistrationView.as_view(),name="rest_name_register"),
    path('auth/signup/', include('rest_auth.registration.urls'), name='account_signup'),
    
    path('',include('appCliente.urls')),
    path('',include('appProprietario.urls')),

    re_path(r'registration/account-confirm-email/', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    re_path(r'registration/account-confirm-email/(?P<key>[-:\w]+)/', VerifyEmailView.as_view(),
            name='account_confirm_email')

   
]
