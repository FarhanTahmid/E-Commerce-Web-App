from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS
from system.manage_error_log import ManageErrorLog
from orders.models import Cart, CartItems, Product_SKU
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied as DRFPermissionDenied
from django.core.exceptions import PermissionDenied
from django.db import transaction
from rest_framework.response import Response
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

class CartOwnerPermission(BasePermission):
    """
    Permission that allows both authenticated and guest access to the cart.

    Rules:
      - Read-only operations (GET, HEAD, OPTIONS) are allowed for everyone.
      - For authenticated users, the cart must belong to `request.user`.
      - For guest users, the cart IP must match their current IP.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return obj.customer_id == request.user

        client_ip = get_client_ip(request)
        return obj.device_ip == client_ip


class CartMergeError(Exception):
    """Custom exception for merge failures during guest-to-user cart merging."""
    pass

class InsufficientStockError(Exception):
    """Raised when requested quantity exceeds available stock."""
    pass


class UserCartViewSet(viewsets.ViewSet):
    """
    ViewSet for handling User Carts in the system.

    This ViewSet provides endpoints to:
      - Create or fetch a cart (`create_or_fetch`)
      - Add products to a cart (`add_product`)
      - Update cart item quantities (`update_item`)
      - Remove specific items from a cart (`remove_item`)
      - Clear the entire cart (`clear_cart`)

    Authentication:
      - Uses `SafeJWTAuthentication` to allow "guest" usage if token is invalid/absent.
      - For authenticated requests, uses JWT to identify the user.

    Permissions:
      - `CartOwnerPermission` ensures only the cart's owner (by user or IP) can modify it.
      - `AllowAny` is used specifically for `create_or_fetch`, so guests can create a cart.

    Typical Response Format:
      {
          "id": <cart_id>,
          "cart_total_amount": <decimal>,
          "items": [
              {
                  "id": <cart_item_id>,
                  "product_sku": <sku_pk>,
                  "quantity": <quantity_in_cart>,
                  "product_details": {
                      "name": <product_name>,
                      "price": <price_string>,
                      "sku": <sku_string>,
                      "color": <color>,
                      "size": <size>
                  }
              },
              ...
          ]
      }
    """
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [CartOwnerPermission]

    def get_permissions(self):
        """
        Override ViewSet permissions for specific actions.
        - `create_or_fetch`: anyone can call (guest or authenticated).
        - Others: default to `CartOwnerPermission`.
        """
        if self.action == 'create_or_fetch':
            return [AllowAny()]
        return super().get_permissions()

    def get_object(self):
        """
        Fetch a single Cart object based on the URL pk. Also invokes permission checks.

        Raises:
            404 if cart not found, or 403 if user doesn't have access.
        """
        queryset = Cart.objects.all()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def _merge_carts(self, source_cart, target_cart):
        """
        Merge items from a guest cart (source) into a user cart (target).

        Ensures stock validation for each SKU. If a SKU already exists
        in the target cart, the quantities are summed. If the final
        quantity exceeds current stock, raises InsufficientStockError.

        Args:
            source_cart (Cart): The guest cart to merge from.
            target_cart (Cart): The user cart to merge into.

        Raises:
            InsufficientStockError: If any item exceeds available stock.
        """
        with transaction.atomic():
            for source_item in source_cart.cartitems_set.select_related('product_sku').all():
                sku = source_item.product_sku
                current_stock = sku.product_stock

                target_item = target_cart.cartitems_set.filter(product_sku=sku).first()
                if target_item:
                    new_quantity = target_item.quantity + source_item.quantity
                    if new_quantity > current_stock:
                        raise InsufficientStockError(
                            f"Not enough stock for {sku}. "
                            f"Available: {current_stock}, Requested: {new_quantity}"
                        )
                    target_item.quantity = new_quantity
                    target_item.save()
                else:
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
            # Remove the guest cart once successfully merged
            source_cart.delete()

    @action(detail=False, methods=['post'])
    def create_or_fetch(self, request):
        """
        Create or fetch a cart.

        **URL**: POST /client_api/customer-cart/create_or_fetch/

        **Behavior**:
          - **Guest user**: Cart is identified by IP.
            - The IP address is extracted from X-Forwarded-For or REMOTE_ADDR.
            - If a cart for this IP doesn't exist, a new one is created (201).
            - If it does exist, returns that cart (200).
          - **Authenticated user**: 
            - First checks if there's a guest cart under the same IP. If found, merges it into the user's cart (transfer items, then delete guest cart).
            - Returns the existing or newly-created user cart.

        **Request**:
          - No JSON body required.
          - If authenticated, must include Bearer token in headers. 
          - If guest, can rely on IP.

        **Responses**:
          - 201: Cart newly created (no merges).
          - 200: Cart fetched or merged from guest cart.
          - 400: Insufficient stock error if merging fails (stock issues).
          - 403: If permission check fails for some reason (rare here).
          - 500: Unexpected errors (e.g., DB issues).

        **Example**:
          >>> POST /client_api/customer-cart/create_or_fetch/
          >>> (guest IP scenario)
          {
              "id": 3,
              "cart_total_amount": "0.00",
              "items": []
          }
        """
        try:
            with transaction.atomic():
                user = request.user if request.user.is_authenticated else None
                ip = get_client_ip(request)
                merged = False

                if user:
                    guest_cart = Cart.objects.filter(
                        device_ip=ip,
                        cart_checkout_status=False,
                        customer_id__isnull=True
                    ).first()

                    user_cart, created = Cart.objects.get_or_create(
                        customer_id=user,
                        cart_checkout_status=False,
                        defaults={'device_ip': ip}
                    )

                    if guest_cart:
                        self._merge_carts(guest_cart, user_cart)
                        merged = True

                    cart = user_cart

                else:
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

        except InsufficientStockError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except CartMergeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # Re-raise so DRF returns 403
        except Exception as e:
            return Response(
                {'error': f'Cart operation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        """
        Add a product to the specified cart.

        **URL**: POST /client_api/customer-cart/{cart_id}/add_product/

        **Request Body** (JSON):
          {
            "sku_id": <ProductSKU_PK>,
            "quantity": <int>
          }

        **Headers**:
          - If authenticated, "Authorization: Bearer <token>" must be provided.
          - Otherwise, rely on IP if cart is a "guest" cart.

        **Responses**:
          - 200: Returns the updated cart (same structure as CartSerializer).
          - 400: If 'sku_id' is invalid, or 'quantity' is out of range or exceeds stock.
          - 403: If the user does not own this cart (permission denied).
          - 500: Any other unexpected error.

        **Example**:
          >>> POST /client_api/customer-cart/1/add_product/
          >>> {
          ...     "sku_id": 2,
          ...     "quantity": 3
          ... }
          Returns updated cart data if successful.
        """
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

        except InsufficientStockError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['put'])
    def update_item(self, request, pk=None):
        """
        Update the quantity of a specific item in the cart.

        **URL**: PUT /client_api/customer-cart/{cart_id}/update_item/

        **Request Body** (JSON):
          {
            "item_id": <CartItem_PK>,
            "quantity": <int>
          }

          - If "quantity" is 0, the item will be removed from the cart.
          - If "quantity" > stock, returns 400.

        **Responses**:
          - 200: Updated cart details.
          - 400: If quantity invalid or exceeding stock, or if "item_id" is missing.
          - 404: If the item_id doesn't exist in the given cart.
          - 403: Permission denied if the user/guest doesn't own the cart.
          - 500: Any other unexpected error.

        **Example**:
          >>> PUT /client_api/customer-cart/1/update_item/
          >>> {
          ...     "item_id": 10,
          ...     "quantity": 5
          ... }
        """
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

        except (PermissionDenied, DRFPermissionDenied):
            raise
        except Exception as e:
            return Response(
                {'error': 'Failed to update cart item'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        """
        Remove a specific item from the cart by item_id.

        **URL**: DELETE /client_api/customer-cart/{cart_id}/remove_item/?item_id={item_id}

        **Query Parameter**:
          - `item_id`: The primary key of CartItems to remove.

        **Responses**:
          - 200: Returns updated cart after removal.
          - 400: Missing item_id parameter.
          - 404: Item not found in the cart.
          - 403: Permission denied (cart doesn't belong to user/guest).
          - 500: Unexpected server error.

        **Example**:
          >>> DELETE /client_api/customer-cart/1/remove_item/?item_id=10
        """
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

        except (PermissionDenied, DRFPermissionDenied):
            raise
        except Exception as e:
            return Response(
                {'error': 'Failed to remove item from cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['delete'])
    def clear_cart(self, request, pk=None):
        """
        Clear (delete) all items from the user's cart.

        **URL**: DELETE /client_api/customer-cart/{cart_id}/clear_cart/

        **Responses**:
          - 200: {"message": "Cart has been cleared successfully"}
          - 403: If cart isn't owned by user or IP.
          - 500: Unexpected server error.

        **Example**:
          >>> DELETE /client_api/customer-cart/5/clear_cart/
          >>> {
          ...     "message": "Cart has been cleared successfully"
          ... }
        """
        try:
            with transaction.atomic():
                cart = self.get_object()
                cart.cartitems_set.all().delete()

                return Response(
                    {"message": "Cart has been cleared successfully"},
                    status=status.HTTP_200_OK
                )
        except (PermissionDenied, DRFPermissionDenied):
            raise
        except Exception as e:
            return Response(
                {"error": "Failed to clear cart"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )