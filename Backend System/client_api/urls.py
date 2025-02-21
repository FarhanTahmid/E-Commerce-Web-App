from django.urls import path,include
from .views import *
from .api_view_cart import *
from .api_view_orders import *
from .api_view_product import *
from rest_framework.routers import DefaultRouter

app_name='client_api'

router=DefaultRouter()
router.register(r'customer-cart',UserCartViewSet,basename='customer_cart')
router.register(r'customer-order',OrderViewSet,basename='customer_order')
router.register(r'products',ProductViewSet,basename='products')

urlpatterns = [
    path('', include(router.urls)),    
    path('product-categories/',ProductCategoryListView.as_view(),name='product_category_list')
]
