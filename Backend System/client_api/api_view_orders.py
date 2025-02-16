from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import uuid
from orders.models import Order, OrderDetails, OrderShippingAddress, OrderPayment, Cart, CartItems
from customer.models import Coupon, CustomerAddress
from system.models import Accounts
from rest_framework.permissions import BasePermission
from products.product_management import ManageProducts
from products.models import *

from orders.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderCancelSerializer,
    CouponApplySerializer,
    AddressSerializer
)

def generate_order_id(username, cart_pk):
    return f"#ORD-{username[:4]}-{cart_pk}-{uuid.uuid4().hex[:4].upper()}"

#PAY-COD:ORDERDETAILS
#PAY-CARD:ORDERDETAILs
#PAY-KASH:ORDERDETAILs
#PAY-CPN:PAYMENTMETHID:ORDERDETAILS
#PAY-DIS:
def generate_payment_reference(order_id,COD=False,CPN=False,DIS=False,CARD="",mobile_banking=""):
    
    message = ""

    if COD:
        message= f'PAY-COD:{order_id}'
    elif CARD:
        message=  f'PAY-CARD:{CARD.upper()}-{order_id}'
    elif mobile_banking:
        message=  f'PAY-{mobile_banking.upper()}:{order_id}'
    
    if CPN:
        message+=  f';CPN:APPLIED'
    if DIS:
        message+=  f';DIS:APPLIED'

    return message

class CustomOrderPermission(BasePermission):
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Ensure the user can only access their own orders
        return obj.customer_id == request.user

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomOrderPermission]

    def get_queryset(self):
        return self.queryset.filter(customer_id=self.request.user)

    @action(detail=False, methods=['post'], url_path='checkout')
    def create_order(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                # Get user's cart
                cart = Cart.objects.get(
                    customer_id=request.user,
                    cart_checkout_status=False
                )
                cart_items = CartItems.objects.filter(cart_id=cart)
                
                # Validate cart items
                for item in cart_items:
                    if item.quantity > item.product_sku.product_stock:
                        return Response(
                            {'error': f'Insufficient stock for {item.product_sku.product_sku}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                # Generate order ID using cart PK
                order_id = generate_order_id(request.user.username, cart.pk)

                # Handle shipping address
                address_data = serializer.validated_data.get('shipping_address')
                save_address = serializer.validated_data.get('save_address', False)
                
                if serializer.validated_data.get('use_saved_address'):
                    try:
                        address = CustomerAddress.objects.get(customer_id=request.user)
                        address_data = AddressSerializer(address).data
                        #excluding address title for OrderShippmentModel
                        address_data = {
                            "address_line1": address_data["address_line1"],
                            "address_line2": address_data["address_line2"],
                            "country": address_data["country"],
                            "city": address_data["city"],
                            "postal_code": address_data["postal_code"],
                        }
                    except CustomerAddress.DoesNotExist:
                        return Response(
                            {'error': 'No saved address found'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    if save_address:
                        address_serializer = AddressSerializer(data=address_data)
                        address_serializer.is_valid(raise_exception=True)
                        address = address_serializer.save(customer_id=request.user)
                
                # Apply coupon
                coupon_code = serializer.validated_data.get('coupon_code')
                coupon = None
                if coupon_code:
                    try:
                        coupon = Coupon.objects.get(
                            coupon_code=coupon_code,
                            customer_id=request.user,
                            start_date__lte=timezone.now(),
                            end_date__gte=timezone.now()
                        )
                        if coupon.usage_limit <= 0:
                            return Response(
                                {'error': 'Coupon usage limit exceeded'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    except Coupon.DoesNotExist:
                        return Response(
                            {'error': 'Invalid or expired coupon'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                # Calculate totals
                total_amount_before_discount_and_coupon = float(cart.cart_total_amount)
                total_amount = cart.cart_total_amount
                discount_amount = 0
                coupon_discount_amount = 0

                if coupon:
                    if coupon.discount_type == 'percentage':
                        discount_amount = float(total_amount) * float((coupon.discount_percentage / 100))
                        if coupon.maximum_discount_amount:
                            discount_amount = min(discount_amount, coupon.maximum_discount_amount)
                    elif coupon.discount_type == 'fixed':
                        discount_amount = coupon.discount_amount
                    
                    coupon_discount_amount = float(discount_amount)
                    total_amount -= discount_amount
                    coupon.usage_limit -= 1
                    coupon.save()

                #checking for discount
                applied_discount = False
                total_discount_amount = 0
                for item in cart_items:
                    product_id = item.product_sku.product_id
                    active_discount,message = ManageProducts.fetch_product_discount(product_id=product_id.pk)
                    if active_discount:
                        applied_discount = True
                        active_discount = active_discount[0]
                        total_discount_amount += (item.quantity) * active_discount.discount_amount

                total_amount -= total_discount_amount


                # Create order
                order = Order.objects.create(
                    order_id=order_id,
                    customer_id=request.user,
                    total_amount=total_amount,
                    order_status='pending'
                )
                # Create order details
                for item in cart_items:
                    OrderDetails.objects.create(
                        order_id=order,
                        product_sku=item.product_sku,
                        quantity=item.quantity,
                        subtotal=item.product_sku.product_price * item.quantity
                    )
                    # Update stock
                    item.product_sku.product_stock -= item.quantity
                    item.product_sku.save()

                # Create shipping address
                OrderShippingAddress.objects.create(
                    order_id=order,
                    **address_data
                )
                # Create payment record
                payment_mode = serializer.validated_data['payment_mode']
                payment_reference = ""
                if payment_mode == 'cash_on_delivery' or payment_mode == 'Cash On Delivery':
                    payment_reference = generate_payment_reference(order_id=order,COD=True,CPN=True if coupon_discount_amount>0 else False, DIS=True if applied_discount else False)
                elif payment_mode == 'bkash' or payment_mode == 'rocket' or payment_mode == 'nagad' or payment_mode == 'wallet' or payment_mode=='net_banking' or payment_mode=='Net Banking':
                    payment_reference = generate_payment_reference(order_id=order,mobile_banking=payment_mode,CPN=True if coupon_discount_amount>0 else False, DIS=True if applied_discount else False)
                elif payment_mode == 'credit_card' or payment_mode == 'Credit Card' or payment_mode == 'debit_card' or payment_mode == 'Debit Card':
                    payment_reference = generate_payment_reference(order_id=order,CARD=payment_mode,CPN=True if coupon_discount_amount>0 else False, DIS=True if applied_discount else False)
                OrderPayment.objects.create(
                    order_id=order,
                    coupon_applied = coupon,
                    payment_mode=payment_mode,
                    payment_status='pending' if payment_mode == 'cash_on_delivery' else 'success',
                    payment_amount=total_amount,
                    payment_reference=payment_reference
                )
                # Mark cart as checked out
                cart.cart_checkout_status = True
                cart.save()

                order_serializer = OrderSerializer(order,context={'request': request}).data
                response = {
                    'order id':order_serializer['order_id'],
                    'order date':order_serializer['order_date'],
                    'total':total_amount_before_discount_and_coupon,
                    'coupon amount': coupon_discount_amount,
                    'discount':total_discount_amount,
                    'Net total':order_serializer['total_amount'],
                    'order status':order_serializer['order_status'],
                    'shipping_address':order_serializer['shipping_address'],
                    'payment details':order_serializer['payment_details'],

                }

                return Response(data=response, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response(
                {'error': 'No active cart found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        serializer = OrderCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        time_since_order = timezone.now() - order.order_date
        cancellation_window = timedelta(hours=2)

        try:
            with transaction.atomic():
                if time_since_order <= cancellation_window:
                    order.order_status = 'cancelled'
                    order.save()
                    
                    # Restore stock
                    order_details = OrderDetails.objects.filter(order_id=order)
                    for detail in order_details:
                        detail.product_sku.product_stock += detail.quantity
                        detail.product_sku.save()
                    
                    # Handle payment reversal if needed
                    payment = OrderPayment.objects.get(order_id=order)
                    if payment.payment_status == 'success':
                        payment.payment_status = 'refunded'
                        payment.save()

                    #restore coupon if used
                    if payment.coupon_applied:
                        payment.coupon_applied.usage_limit+=1
                        payment.coupon_applied.save()
                        payment.save()

                    return Response(
                        {'message': 'Order cancelled successfully'},
                        status=status.HTTP_200_OK
                    )
                else:
                    # Create cancellation request
                    cancellation_reason = serializer.validated_data['reason']
                    # Implement cancellation request workflow here
                    return Response(
                        {'message': 'Cancellation request submitted for approval'},
                        status=status.HTTP_200_OK
                    )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], url_path='apply-coupon')
    def apply_coupon(self, request, pk=None):
        order = self.get_object()
        serializer = CouponApplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            coupon = Coupon.objects.get(
                coupon_code=serializer.validated_data['coupon_code'],
                customer_id=request.user,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            )

            if coupon.usage_limit <= 0:
                return Response(
                    {'error': 'Coupon usage limit exceeded'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Calculate discount
            total_amount = order.total_amount
            discount_amount = 0

            if coupon.discount_type == 'percentage':
                discount_amount = total_amount * (coupon.discount_percentage / 100)
                if coupon.maximum_discount_amount:
                    discount_amount = min(discount_amount, coupon.maximum_discount_amount)
            elif coupon.discount_type == 'fixed':
                discount_amount = coupon.discount_amount

            # Update order total
            order.total_amount = total_amount - discount_amount
            order.save()

            # Update coupon usage
            coupon.usage_limit -= 1
            coupon.save()

            return Response(OrderSerializer(order).data)

        except Coupon.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired coupon'},
                status=status.HTTP_400_BAD_REQUEST
            )