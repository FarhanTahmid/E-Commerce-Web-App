from django.urls import path,include
from .views import *
from .api_view_cart import *
from .api_view_orders import *
from .api_view_product import *
from .api_view_wishlist import *
from .api_view_invoice_download import *
from rest_framework.routers import DefaultRouter

app_name='client_api'

router=DefaultRouter()
router.register(r'customer-wishlist',UserWishlistViewSet,basename='customer_wishlist')
router.register(r'customer-cart',UserCartViewSet,basename='customer_cart')
router.register(r'customer-order',OrderViewSet,basename='customer_order')
router.register(r'fetch',FetchViewSet,basename='fetch')

urlpatterns = [
    path('', include(router.urls)),
    path('customer-order/<str:order_id>/invoice/', UserInvoiceDownloadView.as_view(), name='user_invoice_download'),
    path('customer-order/<str:order_id>/invoice/preview/', UserInvoicePreviewView.as_view(), name='user_invoice_preview'),
    path('customer-order/invoices/', UserInvoiceListView.as_view(), name='user_invoice_list'),
    
    path('product-categories/',ProductCategoryListView.as_view(),name='product_category_list')
]
