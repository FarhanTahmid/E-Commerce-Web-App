from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS
from system.manage_error_log import ManageErrorLog
from orders.models import Cart, CartItems, Product_SKU
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction
from rest_framework.response import Response
from orders.serializers import CartSerializer
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied

logging = ManageErrorLog()

def get_client_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class SafeJWTAuthentication(JWTAuthentication):
    """JWT authentication that doesn't raise exceptions for unverified tokens"""
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            return None  # Treat invalid/expired tokens as anonymous

class CartOwnerPermission(BasePermission):
    """Permission that allows both authenticated and guest access"""
    def has_object_permission(self, request, view, obj):
        # Allow read-only for all
        if request.method in SAFE_METHODS:
            return True

        # For authenticated users
        if request.user.is_authenticated:
            return obj.customer_id == request.user

        # For guests - strict IP matching
        client_ip = get_client_ip(request)
        return obj.device_ip == client_ip

class CartMergeError(Exception):
    """Custom exception for merge failures"""
    pass

class InsufficientStockError(Exception):
    """Exception for stock validation failures"""
    pass


class UserCartViewSet(viewsets.ViewSet):
    authentication_classes = [SafeJWTAuthentication]  # Use our custom auth
    permission_classes = [CartOwnerPermission]

    def get_permissions(self):
        # Special case for create_or_fetch
        if self.action == 'create_or_fetch':
            return [AllowAny()]
        return super().get_permissions()

    def get_object(self):
        """Get cart with JWT/IP validation"""
        queryset = Cart.objects.all()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def _merge_carts(self, source_cart, target_cart):
        """Merge items from source_cart into target_cart with real-time stock validation."""
        try:
            with transaction.atomic():
                # For each item in the source cart
                for source_item in source_cart.cartitems_set.select_related('product_sku').all():
                    sku = source_item.product_sku
                    current_stock = sku.product_stock

                    # Check if target cart already has this SKU
                    target_item = target_cart.cartitems_set.filter(product_sku=sku).first()

                    if target_item:
                        # Add quantities together
                        new_quantity = target_item.quantity + source_item.quantity
                        if new_quantity > current_stock:
                            raise InsufficientStockError(
                                f"Not enough stock for {sku}. "
                                f"Available: {current_stock}, Requested: {new_quantity}"
                            )
                        target_item.quantity = new_quantity
                        target_item.save()
                    else:
                        # If it's a new SKU for the target cart
                        if source_item.quantity > current_stock:
                            raise InsufficientStockError(
                                f"Not enough stock for {sku}. "
                                f"Available: {current_stock}, Requested: {source_item.quantity}"
                            )
                        CartItems.objects.create(
                            cart_id=target_cart,
                            product_sku=sku,
                            quantity=source_item.quantity
                        )
                # Delete the source cart after merging
                source_cart.delete()

        except Exception as e:
            raise CartMergeError(f"Cart merge aborted: {str(e)}") from e

    @action(detail=False, methods=['post'])
    def create_or_fetch(self, request):
        """
        For guest users:
           - Create/fetch cart by IP.
        For authenticated users:
           - If a guest cart exists for the same IP, merge it into the user cart.
           - Then return/create the user cart.
        """
        try:
            with transaction.atomic():
                user = request.user if request.user.is_authenticated else None
                ip = get_client_ip(request)
                merged = False

                if user:
                    # Check for a guest cart with the same IP
                    guest_cart = Cart.objects.filter(
                        device_ip=ip,
                        cart_checkout_status=False,
                        customer_id__isnull=True
                    ).first()

                    # Create or fetch the user's cart
                    user_cart, created = Cart.objects.get_or_create(
                        customer_id=user,
                        cart_checkout_status=False,
                        defaults={'device_ip': ip}
                    )

                    # Merge if guest cart exists
                    if guest_cart:
                        self._merge_carts(guest_cart, user_cart)
                        merged = True

                    cart = user_cart

                else:
                    # Guest user
                    cart, created = Cart.objects.get_or_create(
                        device_ip=ip,
                        cart_checkout_status=False
                    )

                status_code = (
                    status.HTTP_201_CREATED 
                    if (created and not merged) 
                    else status.HTTP_200_OK
                )
                return Response(CartSerializer(cart).data, status=status_code)

        except Exception as e:
            return Response(
                {'error': f'Cart operation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        """Add product to cart with stock validation"""
        try:
            with transaction.atomic():
                cart = self.get_object()
                serializer = CartSerializer(cart)

                try:
                    sku_id = request.data['sku_id']
                    quantity = int(request.data.get('quantity', 1))
                    sku = Product_SKU.objects.select_for_update().get(pk=sku_id)
                except (KeyError, Product_SKU.DoesNotExist, ValueError):
                    return Response(
                        {'error': 'Invalid product or quantity'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if quantity < 1:
                    return Response(
                        {'error': 'Quantity must be at least 1'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if quantity > sku.product_stock:
                    return Response(
                        {'error': 'Insufficient stock'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Get or create the cart item
                item, created = CartItems.objects.get_or_create(
                    cart_id=cart,
                    product_sku=sku,
                    defaults={'quantity': quantity}
                )

                # If item already exists, update quantity
                if not created:
                    new_quantity = item.quantity + quantity
                    if new_quantity > sku.product_stock:
                        return Response(
                            {'error': 'Exceeds available stock'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    item.quantity = new_quantity
                    item.save()

                return Response(serializer.data)
        except (PermissionDenied, DRFPermissionDenied) as pd:
            # Let DRF handle it; this will become a 403 response
            raise pd
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['put'])
    def update_item(self, request, pk=None):
        """Update cart item quantity with stock validation"""
        try:
            with transaction.atomic():
                cart = self.get_object()
                item_id = request.data.get('item_id')
                new_quantity = int(request.data.get('quantity', 1))

                if new_quantity < 0:
                    return Response(
                        {'error': 'Invalid quantity'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    item = CartItems.objects.select_related('product_sku').get(
                        pk=item_id,
                        cart_id=cart
                    )
                    sku = item.product_sku

                    if new_quantity > sku.product_stock:
                        return Response(
                            {'error': 'Insufficient stock'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    if new_quantity == 0:
                        item.delete()
                    else:
                        item.quantity = new_quantity
                        item.save()

                    return Response(CartSerializer(cart).data)

                except CartItems.DoesNotExist:
                    return Response(
                        {'error': 'Item not found in cart'},
                        status=status.HTTP_404_NOT_FOUND
                    )

        except Exception as e:
            return Response(
                {'error': 'Failed to update cart item'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        """Remove a specific item from the cart."""
        try:
            with transaction.atomic():
                cart = self.get_object()
                item_id = request.query_params.get('item_id')

                if not item_id:
                    return Response(
                        {'error': 'Missing item_id parameter'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    item = CartItems.objects.get(pk=item_id, cart_id=cart)
                    item.delete()
                    return Response(CartSerializer(cart).data)
                except CartItems.DoesNotExist:
                    return Response(
                        {'error': 'Item not found in cart'},
                        status=status.HTTP_404_NOT_FOUND
                    )

        except Exception as e:
            return Response(
                {'error': 'Failed to remove item from cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['delete'])
    def clear_cart(self, request, pk=None):
        """Clear all items from the user's cart."""
        try:
            with transaction.atomic():
                cart = self.get_object()
                cart.cartitems_set.all().delete()  # Delete all cart items

                return Response(
                    {"message": "Cart has been cleared successfully"},
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {"error": "Failed to clear cart"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
