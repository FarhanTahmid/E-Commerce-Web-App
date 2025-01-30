from rest_framework import serializers
from .models import Cart, CartItems

class CartItemSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ['id', 'product_sku', 'quantity', 'product_details']
        read_only_fields = ['id']

    def get_product_details(self, obj):
        return {
            'name': obj.product_sku.product_id.product_name,
            'price': str(obj.product_sku.product_price),
            'sku': obj.product_sku.product_sku,
            'color': obj.product_sku.product_color,
            'size': obj.product_sku.product_size
        }

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitems_set', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'cart_total_amount', 'items']
        read_only_fields = ['id', 'cart_total_amount', 'items']