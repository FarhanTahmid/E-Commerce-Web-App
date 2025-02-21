from rest_framework import serializers
from .models import *
from e_commerce_app import settings
from .product_management import ManageProducts

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
    brand_logo = serializers.SerializerMethodField()

    def get_brand_logo(self, obj):
        if obj.brand_logo:
            request = self.context.get('request')  # Ensure request context is available
            if request:
                return request.build_absolute_uri(f"/{SERVER_API_URL}{settings.MEDIA_URL}{obj.brand_logo}")
        return None

    class Meta:
        model = Product_Brands
        fields = '__all__'

class Product_Flavour_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Flavours
        fields = '__all__'

class Product_SKU_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_SKU
        fields= '__all__'

class Product_Discount_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Discount
        fields = '__all__'

class Product_Images_Serializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    def get_product_image(self, obj):
        if obj.product_image:
            request = self.context.get('request')  # Ensure request context is available
            if request:
                return request.build_absolute_uri(f"/{SERVER_API_URL}{settings.MEDIA_URL}{obj.product_image}")
        return None
    
    class Meta:
        model=Product_Images
        fields= '__all__'
        
class Product_Serializer(serializers.ModelSerializer):

    product_sku = Product_SKU_Serializer(many=True,read_only=True)
    product_discount = Product_Discount_Serializer(many=True,read_only=True)
    product_images = Product_Images_Serializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields= '__all__'

class Product_Detail_Serializer(serializers.ModelSerializer):

    product_sku = serializers.SerializerMethodField()
    product_discount = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields='__all__'

    def get_product_sku(self,obj):
        try:
            product = Product.objects.get(id=obj.pk)
            skus,message = ManageProducts.fetch_product_sku(product_id=product.pk)
            return skus
        except:
            return None
        
    def get_product_discount(self,obj):
        try:
            product = Product.objects.get(id=obj.pk)
            discounts,message = ManageProducts.fetch_product_discount(product_id=product.pk)
            return discounts[0]
        except:
            return None
        
    def get_product_images(self,obj):
        try:
            product = Product.objects.get(id=obj.pk)
            images,message = ManageProducts.fetch_product_image(product_pk=product.pk)
            return images
        except:
            return None
    
