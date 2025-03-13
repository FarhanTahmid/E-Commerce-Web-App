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

    product_category = Product_Category_Serializer(many=True,read_only=True)
    product_sub_category = Product_Sub_Category_Serializer(many=True,read_only=True)
    product_brand = Product_Brands_Serializer(read_only=True)
    product_sku = Product_SKU_Serializer(many=True,read_only=True)
    product_discount = Product_Discount_Serializer(many=True,read_only=True)
    product_images = Product_Images_Serializer(many=True,read_only=True)


    class Meta:
        model = Product
        fields= '__all__'

class Product_Detail_Serializer(serializers.ModelSerializer):

    product_category = Product_Category_Serializer(many=True,read_only=True)
    product_sub_category = Product_Sub_Category_Serializer(many=True,read_only=True)
    product_brand = Product_Brands_Serializer(read_only=True)
    product_discount = serializers.SerializerMethodField()
    product_images= serializers.SerializerMethodField()
    product_flavours = serializers.SerializerMethodField()
    product_skus = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields='__all__'

    def get_product_flavours(self, obj):
        
        flavours = {}
        product_sku = Product_SKU.objects.filter(product_id=obj.pk)
        for sku in product_sku:
            flavour = Product_Flavour_Serializer(sku.product_flavours.all(),many=True).data
            flavours[sku.pk] = flavour
        return flavours
        
    def get_product_discount(self, obj):
        try:
            discounts, message = ManageProducts.fetch_product_discount(product_id=obj.pk)
            if discounts and len(discounts) > 0:
                return Product_Discount_Serializer(discounts[0]).data
            return None
        except Exception as e:
            print(f"Discount error: {e}")
            return None
        
    def get_product_images(self, obj):
        try:
            images, message = ManageProducts.fetch_product_image(product_pk=obj.pk)
            image_list = []
            # Add absolute URLs to the images
            request = self.context.get('request')
            if request and images:
                for image in images:
                    if hasattr(image, 'product_image') and image.product_image:
                        image_list.append(request.build_absolute_uri(
                            f"/{SERVER_API_URL}{settings.MEDIA_URL}{image.product_image}"
                        ))
            return image_list
        except Exception as e:
            return None
        
    def get_product_skus(self, obj):

        try:
            skus, message = ManageProducts.fetch_product_sku(product_id=obj.pk)
            return Product_SKU_Serializer(skus, many=True).data
        except Exception as e:
            return None
    
