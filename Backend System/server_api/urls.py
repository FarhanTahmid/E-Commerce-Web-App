from django.urls import path
from . import views

app_name='server_api'

urlpatterns = [
    #product categories CRUD
    path('product/categories/create/', views.CreateProductCategoryView.as_view(), name='create_product_categories'),
    path('product/categories/fetch_all/',views.FetchProductCategoryView.as_view(),name='fetch_all_product_categories'),
    path('product/categories/<int:pk>/',views.FetchProductCategoryWithPkView.as_view(),name='fetch_a_product_category'),
    path('product/categories/update/<int:pk>/',views.UpdateProductCategoryView.as_view(),name='update_product_categories'),
    path('product/categories/delete/<int:pk>/',views.DeleteProductCategoryView.as_view(),name='delete_product_categories'),

    #product sub categories CRUD
    path('product/sub_categories/fetch_all_product_sub_categories_for_a_category/<int:pk>/', views.FetchProductSubCategoryView.as_view(), name='fetch_all_product_sub_categories_for_a_category'),
    path('product/sub_categories/create/<int:pk>/',views.CreateProductSubCategoryView.as_view(),name='create_product_sub_categories'),
    path('product/sub_categories/update/<int:pk>/',views.UpdateProductSubCategoryView.as_view(),name='update_product_sub_categories'),
    path('product/sub_categories/delete/<int:pk>/',views.DeleteProductSubCategoryView.as_view(),name='delete_product_sub_categories'),
]