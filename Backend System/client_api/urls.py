from django.urls import path,include
from .views import *
from .cart_api_views import *
from rest_framework.routers import DefaultRouter

app_name='client_api'

cart_router=DefaultRouter()
cart_router.register(r'customer-cart',UserCartViewSet,basename='customer_cart')


urlpatterns = [
    path('', include(cart_router.urls)),    
    path('product-categories/',ProductCategoryListView.as_view(),name='product_category_list')
]
