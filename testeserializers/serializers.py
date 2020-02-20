from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryChoice(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class ItemSerializer(serializers.ModelSerializer):
    #activity = serializers.PrimaryKeyRelatedField(many=True,queryset=Category.objects.all())
    #category_name = CategoryChoice(many=True)
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Item
        fields = ('id', 'name','category_name','category')
    
    def create(self, validated_data):
        return Item.objects.create(**validated_data)