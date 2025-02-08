from rest_framework import serializers
from .models import *
from e_commerce_app import settings

SERVER_API_URL = 'server_api'

class Product_Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Category
        fields = '__all__'

class Product_Sub_Category_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product_Sub_Category
        fields = '__all__'

class Product_Brands_Serializer(serializers.ModelSerializer):
    brand_logo_url = serializers.SerializerMethodField()

    def get_brand_logo(self, obj):
        if obj.brand_logo:
            request = self.context.get('request')  # Get the request from context
            domain = request.get_host()
            return f"{domain}/{SERVER_API_URL}{settings.MEDIA_URL}{obj.brand_logo}"
        return None

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
