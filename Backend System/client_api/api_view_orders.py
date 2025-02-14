import uuid
from datetime import datetime
from django.db import transaction
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from orders.models import (
    Order,
    OrderDetails,
    OrderShippingAddress,
    OrderPayment,
    Cart,
    CartItems
)
from orders.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderCancelSerializer,
    CouponApplySerializer,
    AddressSerializer
)

def generate_order_id(username,order_pk):
    return f"#ORD-{username[:4]}-{order_pk}-" + uuid.uuid4().hex[:4].upper()


class OrderViewSet(viewsets.ViewSet):
    """
    A ViewSet to handle order creation (checkout), retrieval, cancellation, etc.

    Endpoints:
      - list (GET /orders/): List all orders belonging to the authenticated user.
      - retrieve (GET /orders/{pk}/): Retrieve a specific order if owned by the user.
      - checkout (POST /orders/checkout/): Create an order from a Cart.
      - cancel (POST /orders/{pk}/cancel/): Cancel an order if still in a cancellable status.
      - (optional) update_shipping_address, add_payment, etc. if you prefer separate endpoints.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /orders/
        Returns all orders belonging to the authenticated user.
        """
        orders = Order.objects.filter(customer_id=request.user).order_by('-order_date')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        GET /orders/{pk}/
        Retrieves a single order if it belongs to the authenticated user.
        """
        try:
            order = Order.objects.get(pk=pk, customer_id=request.user)
        except Order.DoesNotExist:
            raise DRFPermissionDenied("You do not have permission to view this order.")

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        POST /orders/checkout/
        Creates a new order from a provided cart_id.
        
        Expected JSON Body:
          {
            "cart_id": <int>,
            "shipping_address": {
              "address_line1": "...",
              "address_line2": "...",
              "country": "...",
              "city": "...",
              "postal_code": "..."
            },
            "payment": {
              "payment_mode": "...",
              "payment_status": "pending",
              "payment_amount": <decimal>,
              "payment_reference": "...any txn ref..."
            }
          }

        Steps:
          1. Validate the cart belongs to the user.
          2. Generate a unique order_id and create the Order record.
          3. Copy cart items into OrderDetails (with price, quantity).
          4. Optionally deduct stock from Product_SKU (if you want).
          5. Optionally create shipping address record.
          6. Optionally create payment record.
          7. Mark cart as checked out.
        """
        cart_id = request.data.get('cart_id')
        if not cart_id:
            return Response({"error": "Missing 'cart_id' in request data."}, status=status.HTTP_400_BAD_REQUEST)

        shipping_data = request.data.get('shipping_address', {})
        payment_data = request.data.get('payment', {})

        try:
            with transaction.atomic():
                # 1. Fetch cart & check ownership
                cart = Cart.objects.select_for_update().get(pk=cart_id)
                if cart.customer_id != request.user:
                    raise DRFPermissionDenied("Cart does not belong to the authenticated user.")
                if cart.cart_checkout_status:
                    return Response({"error": "Cart has already been checked out."}, status=status.HTTP_400_BAD_REQUEST)

                # 2. Create the Order
                new_order = Order.objects.create(
                    order_id=generate_order_id(),
                    customer_id=request.user,
                    total_amount=0,  # Will calculate below
                    order_status='pending'
                )

                # 3. Copy cart items to OrderDetails
                cart_items = CartItems.objects.select_for_update().filter(cart_id=cart)
                total_amount = 0
                for item in cart_items:
                    sku = item.product_sku
                    if item.quantity > sku.product_stock:
                        return Response(
                            {"error": f"Insufficient stock for SKU {sku.product_sku}."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    # (Optional) Deduct stock
                    sku.product_stock -= item.quantity
                    sku.save()

                    # Calculate line subtotal
                    line_subtotal = sku.product_price * item.quantity
                    total_amount += line_subtotal

                    OrderDetails.objects.create(
                        order_id=new_order,
                        product_sku=sku,
                        quantity=item.quantity,
                        units=1,  # or from item if you store "units" in cart
                        subtotal=line_subtotal
                    )

                # Save total amount
                new_order.total_amount = total_amount
                new_order.save()

                # 4. (optional) Shipping address
                # Only create if user provided shipping fields
                if shipping_data:
                    OrderShippingAddress.objects.create(
                        order_id=new_order,
                        address_line1=shipping_data.get('address_line1', ''),
                        address_line2=shipping_data.get('address_line2', ''),
                        country=shipping_data.get('country', ''),
                        city=shipping_data.get('city', ''),
                        postal_code=shipping_data.get('postal_code', '')
                    )

                # 5. (optional) Payment record
                if payment_data:
                    mode = payment_data.get('payment_mode')
                    amount = payment_data.get('payment_amount', total_amount)
                    ref = payment_data.get('payment_reference', '')
                    OrderPayment.objects.create(
                        order_id=new_order,
                        payment_mode=mode,
                        payment_status=payment_data.get('payment_status', 'pending'),
                        payment_amount=amount,
                        payment_reference=ref
                    )

                # 6. Mark the cart as checked out
                cart.cart_checkout_status = True
                cart.save()

                # Clear cart items, if you want to empty it after checkout
                cart_items.delete()

                # 7. Return the order data
                serializer = OrderSerializer(new_order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({"error": "Invalid 'cart_id'. Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except DRFPermissionDenied as e:
            raise e
        except Exception as e:
            return Response({"error": f"Checkout failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        POST /orders/{pk}/cancel/
        Cancels an order if it's still in a cancellable status (e.g., 'pending').

        Example JSON body:
          {
            "reason": "No longer needed"
          }

        Steps:
          1. Fetch the order, ensure it belongs to the user, and is in 'pending'.
          2. Set status to 'cancelled'.
          3. (Optionally) re-stock items in Product_SKU if desired.
        """
        reason = request.data.get('reason', 'No reason provided')

        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(pk=pk, customer_id=request.user)
                if order.order_status not in ['pending']:
                    return Response(
                        {"error": "Order cannot be cancelled in its current status."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                order.order_status = 'cancelled'
                order.save()

                # Re-stock items
                details = OrderDetails.objects.filter(order_id=order)
                for d in details:
                    d.product_sku.product_stock += d.quantity
                    d.product_sku.save()

                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            raise DRFPermissionDenied("You do not have permission to cancel this order.")
        except Exception as e:
            return Response({"error": f"Could not cancel order: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
