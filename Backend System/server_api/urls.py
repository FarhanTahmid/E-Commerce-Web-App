from django.urls import path
from . import views

app_name='server_api'

urlpatterns = [                                                                                                       #NOTE: FOR FRONTEND DEV TO CONNECT APIS

    #business admin
    path('business-admin/signup/',views.SignupBusinessAdminUser.as_view(),name='create_business_admin_user'),
    path('business-admin/update/<str:admin_user_name>/',views.UpdateBusinessAdminUser.as_view(),name='update_business_admin_user'),
    path('business-admin/login/',views.LoginInBusinessAdminUser.as_view(),name='login_business_admin_user'),
    path('business-admin/logout/',views.LogOutBusinessAdminUser.as_view(),name='logout_business_admin_user'),
    path('business-admin/update-password/<str:admin_user_name>/',views.UpdateBusinessAdminUserPassword.as_view(),name='update_business_admin_user_password'),
    path('business-admin/delete/<str:admin_user_name>/',views.DeleteBusinessAdminUser.as_view(),name='delete_business_admin_user'),

    #business admin postion
    path('business-admin/admin-position/fetch-positions/',views.FetchBusinessAdminPosition.as_view(),name='fetch_business_admin_position'),#pass parameters /?name= OR pk= OR none to retrieve all
    path('business-admin/admin-position/create/',views.CreateBusinessAdminPosition.as_view(),name='create_business_admin_position'),
    path('business-admin/admin-position/update/<int:admin_position_pk>/',views.UpdateBusinessAdminPosition.as_view(),name='update_business_admin_position'),
    path('business-admin/admin-position/delete/<int:admin_position_pk>/',views.DeleteBusinessAdminPosition.as_view(),name='delete_business_admin_position'),

    #business admin postion for user
    path('business-admin/admin-position/fetch-position-for-admin/',views.FetchPositionForAdmin.as_view(),name='fetch_position_for_admin'),#post request, no parameter passing, need to send json
    path('business-admin/admin-position/add-or-update-position-for-admin/',views.AddOrUpdatePositionForAdmin.as_view(),name='add_or_update_position_for_admin'),
    path('business-admin/admin-position/delete-position-for-admin/',views.RemovePositionForAdmin.as_view(),name='deletE_position_for_admin'),

    #business admin permissions
    path('business-admin/admin-permissions/fetch-admin-permissions/',views.FetchBusinessAdminPermission.as_view(),name='fetch_business_admin_permissions'),#pass parameter /?permission_pk= OR permission_name= OR none to retrieve all permissions
    path('business-admin/admin-permissions/create/',views.CreateBusinessAdminPermission.as_view(),name='create_business_admin_permissions'),
    path('business-admin/admin-permissions/update/<int:admin_permission_pk>',views.UpdateBusinessAdminPermission.as_view(),name='update_business_admin_permissions'),
    path('business-admin/admin-permissions/delete/<int:admin_permission_pk>',views.DeleteBusinessAdminPermission.as_view(),name='delete_business_admin_permissions'),

    #business admin role permissions
    path('business-admin/admin-role-permission/fetch-role-permissions/',views.FetchBusinessAdminRolePermission.as_view(),name='fetch_business_admin_role_permissions'),#pass parameter /?admin_role_permission_pk = OR admin_position_pk= OR admin_permission_pk= OR none to retrieve all

    #product categories CRUD
    path('product/categories/create/', views.CreateProductCategoryView.as_view(), name='create_product_categories'),
    path('product/categories/fetch-all/',views.FetchProductCategoryView.as_view(),name='fetch_all_product_categories'),#pass parameters /?pk = OR no paramter to fetch all
    path('product/categories/<int:pk>/',views.FetchProductCategoryWithPkView.as_view(),name='fetch_a_product_category'),#works same as fetch_all with pk as parameter, option or additional to use
    path('product/categories/update/<int:pk>/',views.UpdateProductCategoryView.as_view(),name='update_product_categories'),
    path('product/categories/delete/<int:pk>/',views.DeleteProductCategoryView.as_view(),name='delete_product_categories'),


    #product sub categories CRUD
    path('product/sub-categories/fetch-all-product-sub-categories-for-a-category/<int:pk>/', views.FetchProductSubCategoryView.as_view(), name='fetch_all_product_sub_categories_for_a_category'),
    path('product/sub-categories/create/<int:product_category_pk>/',views.CreateProductSubCategoryView.as_view(),name='create_product_sub_categories'),
    path('product/sub-categories/update/<int:product_sub_category_pk>/',views.UpdateProductSubCategoryView.as_view(),name='update_product_sub_categories'),
    path('product/sub-categories/delete/<int:product_sub_category_pk>/',views.DeleteProductSubCategoryView.as_view(),name='delete_product_sub_categories'),

    #product brand
    path('product/product-brand/fetch-product-brands/',views.FetchProductBrands.as_view(),name='fetch_product_brands'),#pass parameters /?pk= OR /?brand_name= OR no parameter to fetch all
    path('product/product-brand/create/',views.CreateProductBrands.as_view(),name='create_product_brand'),
    path('product/product-brand/update/<int:product_brand_pk>/',views.UpdateProductBrands.as_view(),name='update_product_brand'),
    path('product/product-brand/delete/<int:product_brand_pk>/',views.DeleteProductBrands.as_view(),name='delete_product_brand'),

    #product flavours
    path('product/product-flavour/fetch-product-flavour/',views.FetchProductFlavour.as_view(),name='fetch_product_flavour'),#pass parameters /?pk= OR product_flavour_name= OR no paramter to fetch all
    path('product/product-flavour/create/',views.CreateProductFlavour.as_view(),name='create_product_flavour'),
    path('product/product-flavour/update/<int:product_flavour_pk>/',views.UpdateProductFlavour.as_view(),name='update_product_flavour'),
    path('product/product-flavour/delete/<int:product_flavour_pk>/',views.DeleteProductFlavour.as_view(),name='delete_product_flavour'),

    #product
    path('product/fetch-product/',views.FetchProduct.as_view(),name='fetch_product'),#pass parameters /?pk= OR product_name= OR product_brand_pk= OR product_category_pk_list OR product_sub_category_pk_list Or no paramter to fetch all
    path('product/create/',views.CreateProduct.as_view(),name='create_product'),
    path('product/update/<int:product_pk>/',views.UpdateProduct.as_view(),name='update_product'),
    path('product/delete/<int:product_pk>/',views.DeleteProduct.as_view(),name='delete_product'),

    #product sku
    path('product/product-sku/fetch-product-sku/',views.FetchProductSKU.as_view(),name='product_sku_fetch'),#MUST pass parameter either /?pk= OR product_id= OR  product_name= OR product_sku =
    path('product/product-sku/create/',views.CreateProductSKU.as_view(),name='product_sku_create'),
    path('product/product-sku/update/<int:product_sku_pk>/',views.UpdateProductSKU.as_view(),name='update_product_sku'),
    path('product/product-sku/delete/<int:product_sku_pk>/',views.DeleteProductSKU.as_view(),name='delete_product_sku'),

    #product image
    path('product/product-images/fetch-product-image/',views.FetchProductImages.as_view(),name='fetch_product_images'),#pass parameters either /?product_pk= OR product_image_pk= OR no paramters to fetch all
    path('product/product-images/create/<int:product_id>/',views.CreateProductImages.as_view(),name='create_product_images'),
    path('product/product-image/update/<int:product_image_pk>/',views.UpdateProductImage.as_view(),name='update_product_image'),
    path('product/product-image/delete/<int:product_image_pk>/',views.DeleteProductImage.as_view(),name='delete_product_image'),

    #product discount
    path('product/product-discounts/fetch-product-discount/',views.FetchProductDiscount.as_view(),name='fetch_product_discounts'),#pass parameters either /?product_id= OR discount_name= OR is_active= OR product_discount_pk OR none to fetch all
    path('product/product-discounts/create/<int:product_id>/',views.CreateProductDiscount.as_view(),name='create_product_dicount'),
    path('product/product-discounts/update/<int:product_discount_pk>/',views.UpdateProductDiscount.as_view(),name='update_product_discount'),
    path('product/product-discounts/delete/<int:product_discount_pk>/',views.DeleteProductDiscount.as_view(),name='delete_product_discount'),

]