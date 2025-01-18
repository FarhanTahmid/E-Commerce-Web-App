from django.urls import path
from . import views

app_name='api'

urlpatterns = [
    path('product/create/', views.CreateProductCategoryView.as_view(), name='create_product'),
]