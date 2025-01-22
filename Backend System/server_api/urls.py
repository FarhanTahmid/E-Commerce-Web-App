from django.urls import path
from . import views

app_name='server_api'

urlpatterns = [                                                                                                       #NOTE: FOR FRONTEND DEV TO CONNECT APIS

    #business admin
    path('business_admin/fetch_token/',views.FetchToken.as_view(),name='fetch_token'),
    path('business_admin/signup/',views.SignupBusinessAdminUser.as_view(),name='create_business_admin_user'),
    path('business_admin/login/',views.LoginInBusinessAdminUser.as_view(),name='login_business_admin_user'),
    path('business_admin/logout/',views.LogOutBusinessAdminUser.as_view(),name='logout_business_admin_user'),

    #product categories CRUD
    path('product/categories/create/', views.CreateProductCategoryView.as_view(), name='create_product_categories'),
    path('product/categories/fetch_all/',views.FetchProductCategoryView.as_view(),name='fetch_all_product_categories'),#pass parameters /?pk = OR no paramter to fetch all
    path('product/categories/<int:pk>/',views.FetchProductCategoryWithPkView.as_view(),name='fetch_a_product_category'),#works same as fetch_all with pk as parameter, option or additional to use
    path('product/categories/update/<int:pk>/',views.UpdateProductCategoryView.as_view(),name='update_product_categories'),
    path('product/categories/delete/<int:pk>/',views.DeleteProductCategoryView.as_view(),name='delete_product_categories'),

    #product sub categories CRUD
    path('product/sub_categories/fetch_all_product_sub_categories_for_a_category/<int:pk>/', views.FetchProductSubCategoryView.as_view(), name='fetch_all_product_sub_categories_for_a_category'),
    path('product/sub_categories/create/<int:product_category_pk>/',views.CreateProductSubCategoryView.as_view(),name='create_product_sub_categories'),
    path('product/sub_categories/update/<int:product_sub_category_pk>/',views.UpdateProductSubCategoryView.as_view(),name='update_product_sub_categories'),
    path('product/sub_categories/delete/<int:product_sub_category_pk>/',views.DeleteProductSubCategoryView.as_view(),name='delete_product_sub_categories'),

    #product brand
    path('product/product_brand/fetch_product_brands/',views.FetchProductBrands.as_view(),name='fetch_product_brands'),#pass parameters /?pk= OR /?brand_name= OR no parameter to fetch all
]