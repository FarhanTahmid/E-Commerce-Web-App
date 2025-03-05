from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied as DRFPermissionDenied
from django.core.exceptions import PermissionDenied
from django.db import transaction
from system.manage_error_log import ManageErrorLog
from orders.models import Product_SKU, Cart, CartItems
from orders.models import Wishlist, WishlistItem
from orders.serializers import WishlistSerializer
from orders.serializers import CartSerializer

logging = ManageErrorLog()

def get_client_ip(request):
    """
    Retrieve the client IP address from request headers.
    
    Priority:
    1. X-Forwarded-For header (if present)
    2. Remote-Addr
    
    Returns:
        str: IP address as a string.
    """
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class SafeJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that doesn't raise exceptions for unverified tokens.
    
    Normally, if a token is invalid or expired, `AuthenticationFailed` is raised.
    Here, we catch that and return `None` to treat the request as "guest" (no user).
    """
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            return None  # Treat invalid/expired tokens as anonymous


class WishlistOwnerPermission(BasePermission):
    """
    Permission that allows both authenticated and guest access to the wishlist.
    
    Rules:
      - For authenticated users, the wishlist must belong to `request.user`.
      - For guest users, the wishlist IP must match their current IP.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.customer_id == request.user
        
        client_ip = get_client_ip(request)
        return obj.device_ip == client_ip


class WishlistMergeError(Exception):
    """Custom exception for merge failures during guest-to-user wishlist merging."""
    pass


class UserWishlistViewSet(viewsets.ViewSet):
    """
    ViewSet for handling User Wishlists in the system.
    
    This ViewSet provides endpoints to:
      - Create or fetch a wishlist (`create_or_fetch`)
      - Add products to a wishlist (`add_product`)
      - Remove specific items from a wishlist (`remove_item`)
      - Clear the entire wishlist (`clear_wishlist`)
      - Add wishlist item directly to cart (`add_to_cart`)
      - Add all wishlist items to cart (`add_all_to_cart`)
    
    Authentication:
      - Uses `SafeJWTAuthentication` to allow "guest" usage if token is invalid/absent.
      - For authenticated requests, uses JWT to identify the user.
    
    Permissions:
      - `WishlistOwnerPermission` ensures only the wishlist's owner (by user or IP) can modify it.
      - `AllowAny` is used specifically for `create_or_fetch`, so guests can create a wishlist.
    """
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [WishlistOwnerPermission]
    
    def get_permissions(self):
        """
        Override ViewSet permissions for specific actions.
        - `create_or_fetch`: anyone can call (guest or authenticated).
        - Others: default to `WishlistOwnerPermission`.
        """
        if self.action == 'create_or_fetch':
            return [AllowAny()]
        return super().get_permissions()
    
    def get_object(self):
        """
        Fetch a single Wishlist object based on the URL pk. Also invokes permission checks.
        
        Raises:
            404 if wishlist not found, or 403 if user doesn't have access.
        """
        queryset = Wishlist.objects.all()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def _merge_wishlists(self, source_wishlist, target_wishlist):
        """
        Merge items from a guest wishlist (source) into a user wishlist (target).
        
        If an item already exists in the target wishlist, it is skipped.
        
        Args:
            source_wishlist (Wishlist): The guest wishlist to merge from.
            target_wishlist (Wishlist): The user wishlist to merge into.
        """
        with transaction.atomic():
            for source_item in source_wishlist.wishlist_items.select_related('product_sku').all():
                sku = source_item.product_sku
                
                # Check if this SKU already exists in target wishlist
                if not target_wishlist.wishlist_items.filter(product_sku=sku).exists():
                    # Create a new wishlist item
                    WishlistItem.objects.create(
                        wishlist=target_wishlist,
                        product_sku=sku
                    )
            
            # Remove the guest wishlist once successfully merged
            source_wishlist.delete()
    
    @action(detail=False, methods=['post'])
    def create_or_fetch(self, request):
        """
        Create or fetch a wishlist.
        
        **URL**: POST /client_api/customer-wishlist/create_or_fetch/
        
        **Behavior**:
          - **Guest user**: Wishlist is identified by IP.
            - The IP address is extracted from X-Forwarded-For or REMOTE_ADDR.
            - If a wishlist for this IP doesn't exist, a new one is created (201).
            - If it does exist, returns that wishlist (200).
          - **Authenticated user**: 
            - First checks if there's a guest wishlist under the same IP. If found, merges it into the user's wishlist.
            - Returns the existing or newly-created user wishlist.
        
        **Request**:
          - No JSON body required.
          - If authenticated, must include Bearer token in headers. 
          - If guest, can rely on IP.
        
        **Responses**:
          - 201: Wishlist newly created (no merges).
          - 200: Wishlist fetched or merged from guest wishlist.
          - 400: If merging fails.
          - 403: If permission check fails for some reason (rare here).
          - 500: Unexpected errors (e.g., DB issues).
        """
        try:
            with transaction.atomic():
                user = request.user if request.user.is_authenticated else None
                ip = get_client_ip(request)
                merged = False
                
                if user:
                    guest_wishlist = Wishlist.objects.filter(
                        device_ip=ip,
                        customer_id__isnull=True
                    ).first()
                    
                    user_wishlist, created = Wishlist.objects.get_or_create(
                        customer_id=user,
                        defaults={'device_ip': ip}
                    )
                    
                    if guest_wishlist:
                        self._merge_wishlists(guest_wishlist, user_wishlist)
                        merged = True
                    
                    wishlist = user_wishlist
                
                else:
                    wishlist, created = Wishlist.objects.get_or_create(
                        device_ip=ip,
                        customer_id__isnull=True
                    )
                
                status_code = (
                    status.HTTP_201_CREATED
                    if (created and not merged)
                    else status.HTTP_200_OK
                )
                return Response(WishlistSerializer(wishlist).data, status=status_code)
        
        except WishlistMergeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # Re-raise so DRF returns 403
        except Exception as e:
            logging.log_error(e, level='ERROR')
            return Response(
                {'error': f'Wishlist operation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        """
        Add a product to the specified wishlist.
        
        **URL**: POST /client_api/customer-wishlist/{wishlist_id}/add_product/
        
        **Request Body** (JSON):
          {
            "sku_id": <ProductSKU_PK>
          }
        
        **Headers**:
          - If authenticated, "Authorization: Bearer <token>" must be provided.
          - Otherwise, rely on IP if wishlist is a "guest" wishlist.
        
        **Responses**:
          - 200: Returns the updated wishlist.
          - 400: If 'sku_id' is invalid or not provided.
          - 403: If the user does not own this wishlist (permission denied).
          - 409: If the product is already in the wishlist.
          - 500: Any other unexpected error.
        """
        try:
            with transaction.atomic():
                wishlist = self.get_object()
                
                try:
                    sku_id = request.data['sku_id']
                    sku = Product_SKU.objects.get(pk=sku_id)
                except (KeyError, Product_SKU.DoesNotExist):
                    return Response(
                        {'error': 'Invalid or missing product SKU'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Check if product is already in wishlist
                if wishlist.wishlist_items.filter(product_sku=sku).exists():
                    return Response(
                        {'error': 'Product already in wishlist'},
                        status=status.HTTP_409_CONFLICT
                    )
                
                # Add the product to wishlist
                WishlistItem.objects.create(
                    wishlist=wishlist,
                    product_sku=sku
                )
                
                return Response(WishlistSerializer(wishlist).data)
        
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            logging.log_error(e, level='ERROR')
            return Response(
                {'error': 'Failed to add product to wishlist'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        """
        Remove a specific item from the wishlist by item_id.
        
        **URL**: DELETE /client_api/customer-wishlist/{wishlist_id}/remove_item/?item_id={item_id}
        
        **Query Parameter**:
          - `item_id`: The primary key of WishlistItem to remove.
        
        **Responses**:
          - 200: Returns updated wishlist after removal.
          - 400: Missing item_id parameter.
          - 404: Item not found in the wishlist.
          - 403: Permission denied (wishlist doesn't belong to user/guest).
          - 500: Unexpected server error.
        """
        try:
            with transaction.atomic():
                wishlist = self.get_object()
                item_id = request.query_params.get('item_id')
                
                if not item_id:
                    return Response(
                        {'error': 'Missing item_id parameter'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    item = WishlistItem.objects.get(pk=item_id, wishlist=wishlist)
                    item.delete()
                    return Response(WishlistSerializer(wishlist).data)
                except WishlistItem.DoesNotExist:
                    return Response(
                        {'error': 'Item not found in wishlist'},
                        status=status.HTTP_404_NOT_FOUND
                    )
        
        except (PermissionDenied, DRFPermissionDenied):
            raise
        except Exception as e:
            logging.log_error(e, level='ERROR')
            return Response(
                {'error': 'Failed to remove item from wishlist'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['delete'])
    def clear_wishlist(self, request, pk=None):
        """
        Clear (delete) all items from the user's wishlist.
        
        **URL**: DELETE /client_api/customer-wishlist/{wishlist_id}/clear_wishlist/
        
        **Responses**:
          - 200: {"message": "Wishlist has been cleared successfully"}
          - 403: If wishlist isn't owned by user or IP.
          - 500: Unexpected server error.
        """
        try:
            with transaction.atomic():
                wishlist = self.get_object()
                wishlist.wishlist_items.all().delete()
                
                return Response(
                    {"message": "Wishlist has been cleared successfully"},
                    status=status.HTTP_200_OK
                )
        except (PermissionDenied, DRFPermissionDenied):
            raise
        except Exception as e:
            logging.log_error(e, level='ERROR')
            return Response(
                {"error": "Failed to clear wishlist"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        """
        Add a specific item from the wishlist to the user's cart.
        
        **URL**: POST /client_api/customer-wishlist/{wishlist_id}/add_to_cart/
        
        **Request Body** (JSON):
          {
            "item_id": <WishlistItem_PK>,
            "quantity": <int>  # Optional, defaults to 1
          }
        
        **Responses**:
          - 200: Returns the updated cart.
          - 400: Invalid item_id or quantity, or insufficient stock.
          - 404: Item not found in wishlist.
          - 403: Permission denied.
          - 500: Unexpected server error.
        """
        try:
            with transaction.atomic():
                wishlist = self.get_object()
                user = request.user if request.user.is_authenticated else None
                ip = get_client_ip(request)
                
                # Get the wishlist item
                try:
                    item_id = request.data.get('item_id')
                    quantity = int(request.data.get('quantity', 1))
                    
                    if not item_id:
                        return Response(
                            {'error': 'Missing item_id parameter'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    wishlist_item = WishlistItem.objects.select_related('product_sku').get(
                        pk=item_id, wishlist=wishlist
                    )
                    sku = wishlist_item.product_sku
                except (WishlistItem.DoesNotExist, ValueError):
                    return Response(
                        {'error': 'Invalid wishlist item or quantity'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Validate quantity
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
                
                # Get or create cart for user/guest
                if user:
                    cart, _ = Cart.objects.get_or_create(
                        customer_id=user,
                        cart_checkout_status=False,
                        defaults={'device_ip': ip}
                    )
                else:
                    cart, _ = Cart.objects.get_or_create(
                        device_ip=ip,
                        cart_checkout_status=False,
                    )
                
                # Add item to cart
                cart_item, created = CartItems.objects.get_or_create(
                    cart_id=cart,
                    product_sku=sku,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    new_quantity = cart_item.quantity + quantity
                    if new_quantity > sku.product_stock:
                        return Response(
                            {'error': 'Exceeds available stock'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    cart_item.quantity = new_quantity
                    cart_item.save()
                
                return Response(CartSerializer(cart).data)
        
        except (PermissionDenied, DRFPermissionDenied):
            raise
        except Exception as e:
            logging.log_error(e, level='ERROR')
            return Response(
                {'error': 'Failed to add wishlist item to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def add_all_to_cart(self, request, pk=None):
        """
        Add all items from the wishlist to the user's cart.
        
        **URL**: POST /client_api/customer-wishlist/{wishlist_id}/add_all_to_cart/
        
        **Request Body**: Not required.
        
        **Responses**:
          - 200: Returns the updated cart.
          - 207: Partial success (some items added, some failed).
          - 400: If all items failed to add (e.g., all out of stock).
          - 403: Permission denied.
          - 500: Unexpected server error.
        """
        try:
            with transaction.atomic():
                wishlist = self.get_object()
                user = request.user if request.user.is_authenticated else None
                ip = get_client_ip(request)
                
                # Get wishlist items
                wishlist_items = wishlist.wishlist_items.select_related('product_sku').all()
                
                if not wishlist_items.exists():
                    return Response(
                        {'message': 'Wishlist is empty'},
                        status=status.HTTP_200_OK
                    )
                
                # Get or create cart for user/guest
                if user:
                    cart, _ = Cart.objects.get_or_create(
                        customer_id=user,
                        cart_checkout_status=False,
                        defaults={'device_ip': ip}
                    )
                else:
                    cart, _ = Cart.objects.get_or_create(
                        device_ip=ip,
                        cart_checkout_status=False,
                    )
                
                success_count = 0
                errors = []
                
                for wishlist_item in wishlist_items:
                    sku = wishlist_item.product_sku
                    
                    # Default quantity for wishlist items is 1
                    quantity = 1
                    
                    # Check stock
                    if quantity > sku.product_stock:
                        errors.append({
                            'item_id': wishlist_item.id,
                            'error': f'Insufficient stock for {sku.product_id.product_name} ({sku.product_sku})'
                        })
                        continue
                    
                    # Add to cart
                    try:
                        cart_item, created = CartItems.objects.get_or_create(
                            cart_id=cart,
                            product_sku=sku,
                            defaults={'quantity': quantity}
                        )
                        
                        if not created:
                            new_quantity = cart_item.quantity + quantity
                            if new_quantity > sku.product_stock:
                                errors.append({
                                    'item_id': wishlist_item.id,
                                    'error': f'Adding would exceed available stock for {sku.product_id.product_name}'
                                })
                                continue
                            
                            cart_item.quantity = new_quantity
                            cart_item.save()
                        
                        success_count += 1
                    except Exception as e:
                        errors.append({
                            'item_id': wishlist_item.id,
                            'error': f'Failed to add {sku.product_id.product_name} to cart: {str(e)}'
                        })
                
                response_data = CartSerializer(cart).data
                
                # Determine response status
                if success_count == 0 and errors:
                    # All items failed
                    response_data['errors'] = errors
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                elif errors:
                    # Partial success
                    response_data['message'] = f'Added {success_count} out of {len(wishlist_items)} items to cart'
                    response_data['errors'] = errors
                    return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
                else:
                    # Full success
                    response_data['message'] = f'Successfully added all {success_count} items to cart'
                    return Response(response_data, status=status.HTTP_200_OK)
        
        except (PermissionDenied, DRFPermissionDenied):
            raise
        except Exception as e:
            logging.log_error(e, level='ERROR')
            return Response(
                {'error': 'Failed to add wishlist items to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )