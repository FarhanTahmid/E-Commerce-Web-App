from rest_framework import serializers
from .models import Order, OrderShippingAddress,OrderPayment,OrderDetails,Cart,CartItems
from customer.models import CustomerAddress

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
        fields = ['address_line1', 'address_line2', 'country', 'city', 'postal_code']

class OrderCreateSerializer(serializers.Serializer):
    use_saved_address = serializers.BooleanField(default=False)
    save_address = serializers.BooleanField(default=False)
    shipping_address = AddressSerializer(required=False)
    payment_mode = serializers.ChoiceField(
        choices=OrderPayment.PAYMENT_MODE_CHOICES,
        required=True
    )
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('use_saved_address') and not data.get('shipping_address'):
            raise serializers.ValidationError("Shipping address is required")
        return data

class OrderCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True)

class CouponApplySerializer(serializers.Serializer):
    coupon_code = serializers.CharField(required=True)

class OrderSerializer(serializers.ModelSerializer):
    shipping_address = serializers.SerializerMethodField()
    payment_details = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'order_id', 'order_date', 'total_amount', 'order_status',
            'shipping_address', 'payment_details', 'items'
        ]

    def get_shipping_address(self, obj):
        address = OrderShippingAddress.objects.get(order_id=obj)
        return {
            'address_line1': address.address_line1,
            'address_line2': address.address_line2,
            'city': address.city,
            'country': address.country,
            'postal_code': address.postal_code
        }

    def get_payment_details(self, obj):
        payment = OrderPayment.objects.get(order_id=obj)
        return {
            'payment_mode': payment.payment_mode,
            'status': payment.payment_status,
            'amount': payment.payment_amount
        }

    def get_items(self, obj):
        items = OrderDetails.objects.filter(order_id=obj)
        return [
            {
                'product': item.product_sku.product_sku,
                'quantity': item.quantity,
                'price': item.product_sku.product_price
            } for item in items
        ]