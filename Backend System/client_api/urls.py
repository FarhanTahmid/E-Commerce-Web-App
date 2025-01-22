from django.urls import path
from .views import *

app_name='client_api'

urlpatterns = [
    path('product-categories/',ProductCategoryListView.as_view(),name='product_category_list')
]
