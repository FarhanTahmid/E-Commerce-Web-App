from django.urls import path
from . import views

app_name='api'

urlpatterns = [
    path('product/categories/create/', views.CreateProductCategoryView.as_view(), name='create_product_categories'),
    path('product/categories/fetch_all/',views.FetchProductCategoryView.as_view(),name='fetch_all_product_categories'),
    path('product/categories/update/<int:pk>/',views.UpdateProductCategoryView.as_view(),name='update_product_categories'),
]