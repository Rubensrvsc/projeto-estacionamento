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

class ProcuraCategory(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        print(self.kwargs)
        username = self.kwargs['id']
        return Category.objects.filter(id=username)

class ProcuraItemView(generics.ListAPIView):

    serializer_class = ItemSerializer

    def get_queryset(self):
        print(self.kwargs)
        idd = self.kwargs['id_item']
        item = Item.objects.filter(category=idd)
        print(item)
        return item
