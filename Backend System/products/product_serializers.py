from rest_framework import serializers
from .models import *

class Product_Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Category
        fields = '__all__'

class Product_Sub_Category_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product_Sub_Category
        fields = '__all__'

class Product_Brands_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Product_Brands
        fields = '__all__'

class Product_Flavour_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Flavours
        fields = '__all__'
class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= '__all__'
class Product_SKU_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_SKU
        fields= '__all__'
class Product_Images_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Product_Images
        fields= '__all__'
class Product_Discount_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Discount
        fields = '__all__'
