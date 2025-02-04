from rest_framework import serializers
from .models import Cart, CartItems
from rest_framework import serializers
from .models import Order, OrderDetails

from rest_framework import serializers
from .models import (
    Order,
    OrderDetails,
    OrderShippingAddress,
    OrderPayment
)

class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = [
            'id',
            'product_sku',
            'quantity',
            'units',
            'subtotal',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class OrderShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderShippingAddress
        fields = [
            'id',
            'address_line1',
            'address_line2',
            'country',
            'city',
            'postal_code'
        ]
        read_only_fields = ['id']

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = [
            'id',
            'payment_mode',
            'payment_status',
            'payment_date',
            'payment_amount',
            'payment_reference',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'payment_date', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    """
    Includes nested details, shipping, and payment if you want to
    display them in a single response. This depends on how you do your
    relationships and queries.
    """
    orderdetails_set = OrderDetailsSerializer(many=True, source='orderdetails_set', read_only=True)
    ordershippingaddress_set = OrderShippingAddressSerializer(many=True, source='ordershippingaddress_set', read_only=True)
    orderpayment_set = OrderPaymentSerializer(many=True, source='orderpayment_set', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_id',
            'customer_id',
            'order_date',
            'total_amount',
            'order_status',
            'created_at',
            'updated_at',
            'updated_by',
            # Nested
            'orderdetails_set',
            'ordershippingaddress_set',
            'orderpayment_set'
        ]
        read_only_fields = ['id', 'order_id', 'customer_id', 'order_date', 'created_at', 'updated_at']


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