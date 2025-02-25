from rest_framework import serializers
from .models import (
    Order,
    OrderDetails,
    OrderShippingAddress,
    OrderPayment,
    Cart,
    CartItems,
    DeliveryTime
)

from customer.models import Accounts,CustomerAddress,Coupon
from django.utils import timezone
from products.product_management import ManageProducts

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

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = [
            'id',
            'address_title',
            'address_line1',
            'address_line2',
            'country',
            'city',
            'postal_code'
        ]
        read_only_fields = ['id']

class OrderShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderShippingAddress
        fields = [
            'address_line1',
            'address_line2',
            'country',
            'city',
            'postal_code'
        ]

class OrderPaymentSerializer(serializers.ModelSerializer):
    coupon_applied = serializers.SerializerMethodField()

    class Meta:
        model = OrderPayment
        fields = [
            'payment_mode',
            'coupon_applied',
            'payment_status',
            'payment_amount',
            'payment_reference',
            'payment_date'
        ]
        read_only_fields = fields

    def get_coupon_applied(self,obj):
        return obj.coupon_applied.coupon_code if obj.coupon_applied else None

class OrderDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_sku.product_id.product_name')
    product_sku_code = serializers.CharField(source='product_sku.product_sku')
    unit_price = serializers.DecimalField(
        source='product_sku.product_price',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = OrderDetails
        fields = [
            'product_sku_code',
            'product_name',
            'quantity',
            'unit_price',
            'subtotal'
        ]
        read_only_fields = fields

class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = [
            'coupon_code',
            'discount_type',
            'discount_percentage',
            'discount_amount',
            'maximum_discount_amount',
            'start_date',
            'end_date',
            'usage_limit',
            'is_valid',
            'remaining_days'
        ]
        read_only_fields = fields

    def get_is_valid(self, obj):
        return obj.start_date <= timezone.now() <= obj.end_date and obj.usage_limit > 0

    def get_remaining_days(self, obj):
        if obj.end_date > timezone.now():
            return (obj.end_date - timezone.now()).days
        return 0

class OrderSerializer(serializers.ModelSerializer):
    shipping_address = serializers.SerializerMethodField()
    payment_details = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    applied_coupon = serializers.SerializerMethodField()
    delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'order_id',
            'order_date',
            'total_amount',
            'order_status',
            'shipping_address',
            'payment_details',
            'items',
            'applied_coupon',
            'delivery_time'
        ]
        # read_only_fields = fields
    
    def get_delivery_time(self,obj):
        try:
            order = Order.objects.get(order_id = obj)
            return f"{order.delivery_time.delivery_name} - {order.delivery_time.estimated_delivery_time}"
        except:
            return None

    def get_items(self,obj):

        try:
            items = OrderDetails.objects.filter(order_id=obj)
            return OrderDetailsSerializer(items,many=True).data
        except:
            None

    def get_shipping_address(self, obj):

        try:  
            shipping_address = OrderShippingAddress.objects.get(order_id=obj)
            return OrderShippingAddressSerializer(shipping_address).data
        except:
            return None
        
    def get_payment_details(self,obj):
         
        try:
            payment_details = OrderPayment.objects.get(order_id=obj)
            return OrderPaymentSerializer(payment_details).data
        except:
            None
    
    def get_applied_coupon(self, obj):
        try:
            payment = OrderPayment.objects.get(order_id=obj)
            if payment.payment_reference.startswith('CPN-'):
                return CouponSerializer(obj.coupon).data
        except OrderPayment.DoesNotExist:
            return None

class OrderCreateSerializer(serializers.Serializer):
    use_saved_address = serializers.BooleanField(default=False)
    save_address = serializers.BooleanField(default=False)
    shipping_address = AddressSerializer(required=False)
    payment_mode = serializers.ChoiceField(
        choices=OrderPayment.PAYMENT_MODE_CHOICES,
        required=True
    )
    coupon_code = serializers.CharField(required=False, allow_blank=True)
    delivery_time = serializers.IntegerField(required=True)

    def validate(self, data):
        if not data.get('use_saved_address') and not data.get('shipping_address'):
            raise serializers.ValidationError("Shipping address is required when not using saved address")
        return data

class OrderCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True)
    refund_to_wallet = serializers.BooleanField(default=False)

class CouponApplySerializer(serializers.Serializer):
    coupon_code = serializers.CharField(required=True)

class DeliveryTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model= DeliveryTime
        fields = '__all__'

class OrderDetailSerializerForAdmin(serializers.ModelSerializer):

    order = OrderSerializer(many=True,read_only=True)
    order_details = OrderDetailsSerializer(many=True,read_only=True)
    shipping_address = OrderShippingAddressSerializer(many=True,read_only=True)
    payment_details = OrderPaymentSerializer(many=True,read_only=True)

    def to_representation(self, instance):
        """Manually format the dictionary data into JSON"""
        formatted_data = {}
        for order_id, data_list in instance.items():
            order_instance, order_details, shipping_address, payment_details = data_list

            formatted_data[order_id] = {
                "order": OrderSerializer(order_instance).data,
                "order_details": OrderDetailsSerializer(order_details, many=True).data,
                "shipping_address": OrderShippingAddressSerializer(shipping_address).data,
                "payment_details": OrderPaymentSerializer(payment_details).data
            }

        return formatted_data

    