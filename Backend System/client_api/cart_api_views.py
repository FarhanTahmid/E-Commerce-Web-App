from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated,BasePermission,SAFE_METHODS
from system.manage_error_log import ManageErrorLog
from orders.models import Cart,CartItems,Product_SKU
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied,AuthenticationFailed
from django.db import transaction
from rest_framework.response import Response
from orders.serializers import CartSerializer

logging=ManageErrorLog()

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
        """Merges two carts with comprehensive stock validation and error handling"""
        try:
            with transaction.atomic():
                # Create temporary mapping for stock checks
                stock_map = {
                    item.product_sku: item.product_sku.product_stock
                    for item in target_cart.cartitems_set.all()
                }

                # Process all source cart items
                for source_item in source_cart.cartitems_set.select_related('product_sku').all():
                    current_stock = source_item.product_sku.product_stock
                    target_item = target_cart.cartitems_set.filter(
                        product_sku=source_item.product_sku
                    ).first()

                    if target_item:
                        # Calculate potential new quantity
                        potential_qty = target_item.quantity + source_item.quantity
                        final_qty = min(potential_qty, current_stock)
                        
                        if final_qty > target_item.quantity:
                            target_item.quantity = final_qty
                            target_item.save()
                            stock_map[source_item.product_sku] = final_qty
                    else:
                        # Check if we can add new item
                        if source_item.quantity <= current_stock:
                            CartItems.objects.create(
                                cart_id=target_cart,
                                product_sku=source_item.product_sku,
                                quantity=source_item.quantity
                            )
                            stock_map[source_item.product_sku] = source_item.quantity

                # Verify final stock availability
                self._validate_post_merge_stock(target_cart, stock_map)
                
                # Delete source cart after successful merge
                source_cart.delete()
                
        except Exception as e:
            # logging.create_error_log(error_type=type(e).__name__,error_message=str(e))
            raise CartMergeError("Failed to merge carts") from e

    def _validate_post_merge_stock(self, cart, stock_map):
        """Post-merge validation to ensure data integrity"""
        for item in cart.cartitems_set.select_related('product_sku').all():
            current_stock = item.product_sku.product_stock
            if stock_map.get(item.product_sku, 0) > current_stock:
                raise InsufficientStockError(
                    f"Insufficient stock for {item.product_sku} after merge"
                )
    
    

    @action(detail=False, methods=['post'])
    def create_or_fetch(self, request):
        try:
            with transaction.atomic():
                # Handle both authenticated and guest users
                user = request.user if request.user.is_authenticated else None
                ip = get_client_ip(request)

                # Existing cart lookup logic
                if user:
                    cart, created = Cart.objects.get_or_create(
                        customer_id=user,
                        cart_checkout_status=False,
                        defaults={'device_ip': ip}
                    )
                    # Merge guest cart if exists
                    self._merge_carts(user, ip)
                else:
                    cart, created = Cart.objects.get_or_create(
                        device_ip=ip,
                        cart_checkout_status=False
                    )

                return Response(
                    CartSerializer(cart).data,
                    status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
                )

        except Exception as e:
            # logging.create_error_log(error_type=type(e).__name__ , error_message=str(e))
            print(e)
            return Response(
                {'error': 'Cart operation failed'},
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

                # Get or create cart item
                item, created = CartItems.objects.get_or_create(
                    cart_id=cart,
                    product_sku=sku,
                    defaults={'quantity': quantity}
                )

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

        except Exception as e:
            # logging.create_error_log(error_type=type(e).__name__, error_message=str(e))
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
            # logging.create_error_log(error_type=type(e).__name__, error_message=str(e))
            return Response(
                {'error': 'Failed to update cart item'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        """Remove item from cart"""
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
            # logging.create_error_log(error_type=type(e).__name__, error_message=str(e))
            return Response(
                {'error': 'Failed to remove item from cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    @action(detail=True, methods=['delete'])
    def clear_cart(self, request, pk=None):
        """Clear all items from the user's cart"""
        try:
            with transaction.atomic():
                cart = self.get_object()
                cart.cartitems_set.all().delete()  # Delete all cart items
                
                return Response(
                    {"message": "Cart has been cleared successfully"},
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            # logging.create_error_log(error_type=type(e).__name__, error_message=str(e))
            return Response(
                {"error": "Failed to clear cart"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    