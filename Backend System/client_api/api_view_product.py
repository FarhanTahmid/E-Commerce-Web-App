from rest_framework import  viewsets,status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS
from rest_framework_simplejwt.authentication import JWTAuthentication
from products import product_serializers
from django.db import transaction
from django.db.models import Q
from products.models import *
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied as DRFPermissionDenied
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from products.product_serializers import *

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

class ProductNotFound(Exception):
    pass

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
        
class FetchViewPermission(BasePermission):
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


class FetchViewSet(viewsets.ViewSet):

    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = product_serializers.Product_SKU_Detail_Serializer
    queryset = Product_SKU.objects.all()

    def get_permissions(self):
        
        if self.action in ['fetch_product_with_search','fetch_product_with_brand','fetch_product_with_category','fetch_product_with_sub_category',
                           'fetch_product_with_price','fetch_all_product','fetch_brands','fetch_categories','fetch_sub_categories','fetch_product_with_flavour']:
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=['GET'])
    def fetch_all_product(self, request):
    
        try:
            with transaction.atomic():
                queryset = Product_SKU.objects.all()

                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['GET'])
    def fetch_product_with_search(self, request):
    
        try:
            with transaction.atomic():
                queryset = Product_SKU.objects.all()
                search = request.query_params.get('search',"").strip()

                if search:
                    queryset = queryset.filter(product_id__product_name__icontains=search) or queryset.filter(product_id__product_brand__brand_name__icontains=search) or queryset.filter(product_id__product_category__category_name__icontains=search) or queryset.filter(product_id__product_sub_category__sub_category_name__icontains=search) or queryset.filter(product_price__gte=search) or queryset.filter(product_price__lte=search) or queryset.filter(product_flavours__product_flavour_name=search)

                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['GET'])
    def fetch_product_with_brand(self, request):
        
        try:
            with transaction.atomic():
                queryset = Product_SKU.objects.all()
                brand_name = request.query_params.get('brand_name',"").strip()
                if brand_name:
                    queryset = queryset.filter(product_id__product_brand__brand_name=brand_name)

                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['GET'])
    def fetch_product_with_category(self, request):
        
        try:
            with transaction.atomic():
                queryset = Product_SKU.objects.all()
                category_name = request.query_params.get('category_name',"").strip()
                if category_name:
                    queryset = queryset.filter(product_id__product_category__category_name=category_name)

                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.
                HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['GET'])
    def fetch_product_with_sub_category(self, request):
        
        try:
            with transaction.atomic():
                queryset = Product_SKU.objects.all()
                sub_category_name = request.query_params.get('sub_category_name',"").strip()

                if sub_category_name:
                    queryset = queryset.filter(product_id__product_sub_category__sub_category_name=sub_category_name)

                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['GET'])
    def fetch_product_with_flavour(self, request):
        
        try:
            with transaction.atomic():
                queryset = Product_SKU.objects.all()
                flavour_name = request.query_params.get('flavour_name',"").strip()

                if flavour_name:
                    queryset = queryset.filter(product_flavours__product_flavour_name=flavour_name)

                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['GET'])
    def fetch_product_with_price(self, request):
        
        try:
            with transaction.atomic():
                queryset = Product_SKU.objects.all()
                max_price_ = Product_SKU.objects.all().order_by('-product_price')[0]
                min_price = request.query_params.get('min_price',0)
                max_price = request.query_params.get('max_price',max_price_.product_price)

                queryset = queryset.filter(product_price__gte = min_price,product_price__lte = max_price)

                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['GET'])
    def fetch_brands(self, request):
        try:
            with transaction.atomic():
                queryset = Product_Brands.objects.all()
                brand_name = request.query_params.get('brand_name',"").strip()

                if brand_name!="":
                    queryset = queryset.filter(brand_name=brand_name)
                else:
                    queryset = queryset

                serializer = Product_Brands_Serializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['GET'])
    def fetch_categories(self, request):
        try:
            with transaction.atomic():
                queryset = Product_Category.objects.all()
                category_name = request.query_params.get('category_name',"").strip()

                if category_name!="":
                    queryset = queryset.filter(category_name=category_name)
                else:
                    queryset = queryset

                serializer = Product_Category_Serializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['GET'])
    def fetch_sub_categories(self, request):
        try:
            with transaction.atomic():
                queryset = Product_Sub_Category.objects.all()
                sub_category_name = request.query_params.get('sub_category_name',"").strip()

                if sub_category_name!="":
                    queryset = queryset.filter(sub_category_name=sub_category_name)
                else:
                    queryset = queryset

                serializer = Product_Sub_Category_Serializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except ProductNotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (PermissionDenied, DRFPermissionDenied):
            raise  # 403
        except Exception as e:
            return Response(
                {'error': 'Failed to add product to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





