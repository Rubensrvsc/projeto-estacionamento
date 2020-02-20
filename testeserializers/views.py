from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from .models import *

# Create your views here.

class TesteSerializer(generics.ListAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemSerializerCreate(generics.ListCreateAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class CategorySerializerCreate(generics.ListCreateAPIView):

    queryset = Item.objects.all()
    serializer_class = CategorySerializer
