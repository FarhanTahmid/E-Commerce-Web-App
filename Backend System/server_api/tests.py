from rest_framework.test import APITestCase
from django.test import RequestFactory
from rest_framework import status
from django.utils import timezone
from products.models import *
from products import product_serializers
from business_admin.models import *
from django.db.models import Q
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import datetime
from system.models import *
from rest_framework_simplejwt.tokens import RefreshToken
import time
from business_admin import serializers
from orders.models import *
from decimal import Decimal

# Create your tests here.
class ServerAPITestCases(APITestCase):
    
    def setUp(self):
        self.now = timezone.now()
        self.factory = RequestFactory()
        self.signup_url = '/customer/signup/'  
        self.login_url = '/customer/login/'
        
        # credentials setup for signup testing
        self.dev_valid_email = 'existing@example.com'
        self.dev_valid_password = 'password123'
        
        self.dev_existing_user = Accounts(
            email='devexisting2@example.com',
            username='devexisting_user',
            is_superuser = True
        )
        self.dev_existing_user.set_password('password123')
        self.dev_existing_user.save()

        self.admin_email='admin@gmail.com'
        self.admin_password = '1234'

        self.admin_existing_user = Accounts(
            email='existing_admin@example.com',
            username='existing_admin',
            is_admin = True,
            is_superuser = False
        )
        self.admin_existing_user.set_password('1234')
        self.admin_existing_user.save()
        
        
        # credentials setup for login testing
        self.email = 'user@example.com'
        self.password = 'securepassword123'
        
        self.user = Accounts(
            email=self.email,
            username='user',
            is_superuser = False,
            is_admin=True
        )
        self.user.set_password(self.password)
        self.user.save()

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.notification1 = Notification.objects.create(
            title = "11"
        )
        self.notification1_to1 = NotificationTo.objects.create(to=self.user,notification=self.notification1)
        self.notification1_to2 = NotificationTo.objects.create(to=self.user,notification=self.notification1)


        self.notification2 = Notification.objects.create(
            title = "12"
        )
        self.notification2_to1 = NotificationTo.objects.create(to=self.user,notification=self.notification2)

        self.product_category1 = Product_Category.objects.create(category_name="Skincare", description="Products for skincare", created_at=self.now)
        self.product_category2= Product_Category.objects.create(category_name="Makeup", description="Products for makeup", created_at=self.now)
        self.product_sub_category1 = Product_Sub_Category.objects.create(sub_category_name="Moisturizers", description="Products to moisturize skin", created_at=self.now)
        self.product_sub_category2= Product_Sub_Category.objects.create(sub_category_name="Cleansers", description="Products to cleanse skin", created_at=self.now)

        self.product_sub_category1.category_id.set([self.product_category1,self.product_category2])
        self.product_sub_category2.category_id.set([self.product_category2])

        self.adminposition1 = AdminPositions.objects.create(name="Owner",description="Ownerrr")
        self.adminposition2 = AdminPositions.objects.create(name="Manager",description="GRRR")
        self.admin_permission = AdminPermissions.objects.create(permission_name=AdminPermissions.CREATE)
        self.admin_permission.save()
        self.admin_permission2 = AdminPermissions.objects.create(permission_name=AdminPermissions.UPDATE)
        self.admin_permission2.save()
        self.admin_permission3 = AdminPermissions.objects.create(permission_name=AdminPermissions.VIEW)
        self.admin_permission3.save()

        self.admin_role_permission1 = AdminRolePermission.objects.create(role=self.adminposition1,permission=self.admin_permission)
        self.admin_role_permission1.save()
        self.admin_role_permission2 = AdminRolePermission.objects.create(role=self.adminposition1,permission=self.admin_permission3)
        self.admin_role_permission2.save()
        self.admin_user_role = AdminUserRole.objects.create(user=self.user,role=self.adminposition1)
        self.admin_user_role.save()
        

        self.product_brand1 = Product_Brands.objects.create(brand_name="Loreal", brand_country="USA",brand_description="Loreal Paris",
                                                    brand_established_year= 1909,is_own_brand=False,created_at=self.now)
        self.product_brand2 = Product_Brands.objects.create(brand_name="Dove", brand_country="USA",brand_description="Loreal Paris",
                                                    brand_established_year= 2000,is_own_brand=True,created_at=self.now)
        
        self.product_flavour1 = Product_Flavours.objects.create(product_flavour_name="Vanilla", created_at=self.now)
        self.product_flavour2 = Product_Flavours.objects.create(product_flavour_name="Strawberry", created_at=self.now)

        self.product1 = Product.objects.create(product_name="Dove Cleanser", product_brand=self.product_brand2,
                                            product_description="A cleanser by Dove", product_summary="Gentle cleanser",
                                            product_ingredients="Water, Sodium Laureth Sulfate", product_usage_direction="Use twice daily", created_at=self.now)
        self.product1.product_category.set([self.product_category1])
        self.product1.product_sub_category.set([self.product_sub_category2])

        self.product2 = Product.objects.create(product_name="Dove85 Cleanser", product_brand=self.product_brand1,
                                            product_description="A cleanser by Dove", product_summary="Gentle cleanser",
                                            product_ingredients="Water, Sodium Laureth Sulfate", product_usage_direction="Use twice daily", created_at=self.now)
        self.product2.product_category.set([self.product_category1])
        self.product2.product_sub_category.set([self.product_sub_category1])

        self.product3 = Product.objects.create(product_name="Puta Cleanser", product_brand=self.product_brand1,
                                            product_description="A cleanser by Puta", product_summary="Puta",
                                            product_ingredients="Water", product_usage_direction="Use twice daily", created_at=self.now)


        self.product_sku1 = Product_SKU.objects.create(product_id=self.product1,product_color="white",product_price=25.3,product_stock=100,created_at=self.now)
        self.product_sku2 = Product_SKU.objects.create(product_id=self.product1,product_color="silver",product_price=50,product_stock=50,created_at=self.now)
        self.product_sku1.product_flavours.set([self.product_flavour2])
        self.product_sku2.product_flavours.set([self.product_flavour1])


        self.businessadmin1 = BusinessAdminUser.objects.create(admin_full_name="SAMI",admin_user_name="sami2186",admin_position=self.adminposition1,admin_email="sami2186@example.com"
                                                               )
        self.businessadmin1_user = Accounts.objects.create(username="sami2186",email="sami2186@example.com",is_admin=True)
        self.businessadmin1_user.set_password('1234')
        self.businessadmin1_user.save()

        self.admin_user_role2 = AdminUserRole.objects.create(user=self.businessadmin1_user,role=self.adminposition1)
        self.admin_user_role2.save()

        self.user3 = Accounts(username='zz12',password='1234',email="zz12@gmail.com",is_admin=True)
        self.user3.save()

        self.businessadmin3 = BusinessAdminUser.objects.create(admin_full_name="zz12",admin_position=self.adminposition1,admin_email="zz12@gmail.com",admin_user_name='zz12')
        self.businessadmin3.save()
        
        self.product_image = Product_Images.objects.create(product_id=self.product1)

        self.active_discount = Product_Discount.objects.create(
            discount_name="Active Discount",
            discount_amount=10.00,
            start_date=self.now - datetime.timedelta(days=1),  # Started yesterday
            end_date=self.now + datetime.timedelta(days=10),    # Ends in 10 days
            product_id_pk=1
        )
        self.active_discount.save()
        self.active_discount.product_id.add(self.product1)
        self.active_discount.save()

        # Inactive discount (end date in the past)
        self.inactive_discount = Product_Discount.objects.create(
            discount_name="Inactive Discount",
            discount_amount=5.00,
            start_date=self.now - datetime.timedelta(days=10),  # Started 10 days ago
            end_date=self.now - datetime.timedelta(days=1),      # Ended yesterday
            product_id_pk=2
        )
        self.inactive_discount.save()
        self.inactive_discount.product_id.add(self.product2)
        self.inactive_discount.save()

        # Inactive discount (start date in the future)
        self.future_discount = Product_Discount.objects.create(
            discount_name="Future Discount",
            discount_amount=15.00,
            start_date=self.now + datetime.timedelta(days=1),  # Starts tomorrow
            end_date=self.now + datetime.timedelta(days=10),    # Ends in 10 days
            brand_id_pk = 1
        )
        self.future_discount.save()
        self.future_discount.product_id.add(self.product3)
        self.future_discount.save()


        self.delivery_time1 = DeliveryTime.objects.create(
            delivery_name= "Inside dhaka",
            estimated_delivery_time = "7 days"
        )
        self.delivery_time2 = DeliveryTime.objects.create(
            delivery_name= "Outside dhaka",
            estimated_delivery_time = "10 days"
        )
        self.delivery_time3 = DeliveryTime.objects.create(
            delivery_name= "Internation",
            estimated_delivery_time = "1 months"
        )


        self.customer1 = Accounts.objects.create(username="customer1", email="customer1@example.com")
        self.customer2 = Accounts.objects.create(username="customer2", email="customer2@example.com")
        self.customer3 = Accounts.objects.create(username="customer3", email="customer3@example.com")

        self.order1 = Order.objects.create(
            order_id="ORD001",
            customer_id=self.customer1,
            delivery_time=self.delivery_time1,
            total_amount=Decimal("90.50"),
            order_status="pending",
        )

        self.order2 = Order.objects.create(
            order_id="ORD002",
            customer_id=self.customer2,
            delivery_time=self.delivery_time2,
            total_amount=Decimal("150.00"),
            order_status="shipped",
        )

        self.order3 = Order.objects.create(
            order_id="ORD003",
            customer_id=self.customer3,
            delivery_time=self.delivery_time1,
            total_amount=Decimal("50.75"),
            order_status="delivered",
        )

        # Create order details
        self.order_details1 = OrderDetails.objects.create(
            order_id=self.order1,
            product_sku=self.product_sku1,
            quantity=2,
            units=1,
            subtotal=Decimal("60.00")
        )

        self.order_details2 = OrderDetails.objects.create(
            order_id=self.order2,
            product_sku=self.product_sku2,
            quantity=3,
            units=1,
            subtotal=Decimal("136.50")
        )

        self.order_details3 = OrderDetails.objects.create(
            order_id=self.order3,
            product_sku=self.product_sku2,
            quantity=1,
            units=1,
            subtotal=Decimal("20.75")
        )

        # Create shipping addresses
        self.shipping1 = OrderShippingAddress.objects.create(
            order_id=self.order1,
            address_line1="123 Main St",
            city="New York",
            country="USA",
            postal_code="10001"
        )

        self.shipping2 = OrderShippingAddress.objects.create(
            order_id=self.order2,
            address_line1="456 Elm St",
            city="Los Angeles",
            country="USA",
            postal_code="90001"
        )

        self.shipping3 = OrderShippingAddress.objects.create(
            order_id=self.order3,
            address_line1="789 Oak St",
            city="Chicago",
            country="USA",
            postal_code="60601"
        )

        # Create coupons
        self.coupon1 = Coupon.objects.create(
            coupon_code = 'UNIQUE1',
            discount_type = Coupon.DISCOUNT_TYPE_CHOICES[0][0],#percentage
            discount_percentage=30,
            maximum_discount_amount=100,
            start_date = self.now,
            end_date = self.now + datetime.timedelta(days=10),
            customer_id = self.customer1,
            created_at = self.now

        )

        self.coupon2 = Coupon.objects.create(
            coupon_code = 'UNIQUE2',
            discount_type = Coupon.DISCOUNT_TYPE_CHOICES[1][1],#fixed
            discount_amount=50,
            usage_limit=1,
            maximum_discount_amount=100,
            start_date = self.now + datetime.timedelta(days=-5),
            end_date = self.now + datetime.timedelta(days=20),
            customer_id = self.customer2,
            created_at = self.now

        )

        # Create payments
        self.payment1 = OrderPayment.objects.create(
            order_id=self.order1,
            coupon_applied=self.coupon1,
            payment_mode="credit_card",
            payment_status="success",
            payment_amount=Decimal("81.45"),
            payment_reference="PAY123"
        )

        self.payment2 = OrderPayment.objects.create(
            order_id=self.order2,
            coupon_applied=self.coupon2,
            payment_mode="paypal",
            payment_status="success",
            payment_amount=Decimal("142.50"),
            payment_reference="PAY456"
        )

        self.payment3 = OrderPayment.objects.create(
            order_id=self.order3,
            coupon_applied=None,  # No coupon applied
            payment_mode="debit_card",
            payment_status="pending",
            payment_amount=Decimal("50.75"),
            payment_reference="PAY789"
        )

        self.cancelorder1= CancelOrderRequest.objects.create(
            order_id = self.order1,
            cancellation_reason = "yyy"
        )


    # @staticmethod
    # def generate_test_image(color,size):
    #     """Generate an in-memory image file."""
    #     image = Image.new('RGB', (size * 100, size * 100), color=color)
        
    #     # Save it to a BytesIO buffer
    #     buffer = BytesIO()
    #     image.save(buffer, format='JPEG')
    #     buffer.seek(0)

    #     # Return an InMemoryUploadedFile, which is what Django expects for file uploads
    #     return InMemoryUploadedFile(
    #         buffer,  # File
    #         None,  # Field name
    #         f'{color}_{size}.jpg',  # Filename
    #         'image/jpeg',  # Content type
    #         buffer.getbuffer().nbytes,  # File size
    #         None  # Content type extra
    #     )

    # def test_fetch_all_product_categories(self):
    #     """
    #     Test
    #     for fetching product categories
    #     """

    #     response = self.client.get(f'/server_api/product/categories/fetch-all/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(len(response.data['product_category']),2)
    #     expected_data = Product_Category.objects.all()
    #     returned_data = response.data['product_category']
    #     expected_data_serialized = product_serializers.Product_Category_Serializer(expected_data, many=True).data
    #     self.assertEqual(returned_data, expected_data_serialized)

    #     #single
    #     response = self.client.get(f'/server_api/product/categories/fetch-all/?{self.product_category1.pk}')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     expected_data = Product_Category.objects.get(pk=self.product_category1.pk)
    #     returned_data = response.data['product_category'][0]
    #     expected_data_serialized = product_serializers.Product_Category_Serializer(expected_data, many=False).data
    #     self.assertEqual(returned_data, expected_data_serialized)


    # def test_fetch_a_product_category(self):

    #     """
    #     Test
    #     for fetching a product category
    #     """
    #     response = self.client.get(f'/server_api/product/categories/{self.product_category1.pk}/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     expected_data = Product_Category.objects.get(pk=self.product_category1.pk)
    #     returned_data = response.data['product_category']
    #     expected_data_serialized = product_serializers.Product_Category_Serializer(expected_data, many=False).data
    #     self.assertEqual(returned_data, expected_data_serialized)



    # def test_create_product_categories(self):
    #     """
    #     Test
    #     for creating product categories also for duplicate as well
    #     """
    #     data = {"category_name": "Test Product", "description": "Test Description"}
    #     response = self.client.post('/server_api/product/categories/create/', data,format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"New Product category. Test Product successfully added!")

    #     response = self.client.post('/server_api/product/categories/create/', data,format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Same type exists in Database!","Not Equal")

    # def test_update_product_categories(self):
    #     """
    #     Test
    #     for updating product categories
    #     """
        
    #     data = {"category_name": "Glass Skincare", "description": "Products for glass skincare"}
    #     response = self.client.put(f'/server_api/product/categories/update/{self.product_category1.pk}/', data,format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Product Category updated successfully!")

    # def test_delete_product_categories(self):
    #     """
    #     Test
    #     for deleting product categories
    #     """

    #     response = self.client.delete(f'/server_api/product/categories/delete/{self.product_category2.pk}/')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Product Category deleted successfully!")
    #     self.assertFalse(Product_Category.objects.filter(pk=self.product_category2.pk).exists(),False)

    #     #deleting again
    #     response = self.client.delete(f'/server_api/product/categories/delete/{self.product_category2.pk}/')
    #     self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Product Category does not exist!")

    # #test for product sub categories
    # def test_fetch_all_product_sub_category_for_a_category(self):
    #     """
    #     Test
    #     for fetching product sub categories
    #     """

    #     response = self.client.get(f'/server_api/product/sub-categories/fetch-all-product-sub-categories-for-a-category/{self.product_category2.pk}/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(len(response.data['product_sub_category']),2)
    #     expected_data = Product_Sub_Category.objects.filter(category_id = self.product_category2)
    #     returned_data = response.data['product_sub_category']
    #     expected_data_serialized = product_serializers.Product_Sub_Category_Serializer(expected_data, many=True).data
    #     self.assertEqual(returned_data, expected_data_serialized)

    # def test_create_product_sub_category(self):
    #     """
    #     Test
    #     for creating product sub categories
    #     """
    #     data = {"sub_category_name": "Foundation", "description": "Foundation Description"}
    #     response = self.client.post(f'/server_api/product/sub-categories/create/{self.product_category2.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"New Product sub-category, Foundation successfully added!","Success message is incorrect")
        
    #     #if duplicate
    #     response = self.client.post(f'/server_api/product/sub-categories/create/{self.product_category2.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Same type exists in Database!","Success message is incorrect")
   

    # def test_update_product_sub_category(self):

    #     """
    #       Test
    #     for updating product sub categories
    #     """

    #     data = {"category_pk_list":[self.product_category1.pk],"sub_category_name": "Moisturizers lop", "description": "Moisturizers Description"}
    #     response = self.client.put(f'/server_api/product/sub-categories/update/{self.product_sub_category1.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Product Sub Category updated successfully!","Success message is incorrect")


    # def test_delete_product_sub_category(self):
    #     """
    #       Test
    #     for deleting product sub categories
    #     """
    #     response = self.client.delete(f'/server_api/product/sub-categories/delete/{self.product_sub_category1.pk}/')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Product Sub Category deleted successfully!","Success message is incorrect")

    #     #deleting again
    #     response = self.client.delete(f'/server_api/product/sub-categories/delete/{self.product_sub_category1.pk}/')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Product Sub Category does not exist!","Success message is incorrect")

    # #business_admin login in/signup
    # def test_business_admin_signup(self):
    #     """
    #     Test for signing up business admin
    #     """
    #     data = {
    #         "admin_full_name": "John Doe",
    #         "admin_user_name": "johndoe",
    #         "password": "securepassword",
    #         "confirm_password": "securepassword",
    #         "admin_position_pk": self.adminposition1.pk,
    #         "admin_contact_no": "1234567890",
    #         "admin_email": "john.doe@example.com",
    #     }
    #     response = self.client.post(f'/server_api/business-admin/signup/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"Business Admin created successfully. Redirecting to login page","Success messsage is incorrect")
    #     self.assertEqual(response.data['redirect_url'],"/login-page","Success messsage is incorrect")
    #     #self.assertTrue(User.objects.filter(username="johndoe").exists())
    #     #self.assertTrue(BusinessAdminUser.objects.filter(admin_full_name="John Doe").exists())

    # def test_business_admin_log_in(self):
    #     """
    #     Test for loggin in 
    #     """
    #     data = {
    #         "email":self.email,
    #         "password":self.password
    #     }
    #     response = self.client.post(f'/server_api/business-admin/login/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Login successful","Success message is incorrect")

    #     #incorrect data
    #     data = {
    #         "email":"testuser2@example.com",
    #         "password":"password22"
    #     }
    #     response = self.client.post(f'/server_api/business-admin/login/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],'Account with this email does not exist!')

    #     #no data
    #     data ={
    #         "email":"",
    #         "password":""
    #     }
    #     response = self.client.post(f'/server_api/business-admin/login/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Email or Password must be provided!","Success message is incorrect")

    # def test_logout_successful(self):
    #     """
    #     Test that a user can successfully log out and is redirected to the login page.
    #     """
    #     response = self.client.post(f'/server_api/business-admin/logout/',{'refresh':f'{self.refresh}'})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('redirect_url', response.data) 
    #     self.assertEqual(response.data['redirect_url'], '/server_api/business_admin/login/') 


    # def test_logout_unauthenticated(self):
    #     """
    #     Test that an unauthenticated user cannot access the logout endpoint.
    #     """
    #     self.client.credentials()  
    #     response = self.client.post(f'/server_api/business-admin/logout/')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertIn('detail', response.data) 
    #     self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    # def test_business_admin_update(self):
    #     """
    #     Test for updating business admin
    #     """

    #     data= {'admin_full_name':"TrishaHaque Samuel",'admin_position_pk':self.adminposition1.pk,'admin_email':'testuser2@example.com'}
    #     response = self.client.put(f'/server_api/business-admin/update/{str(self.businessadmin1.admin_user_name)}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Business Admin successfully updated")

    # def test_update_business_admin_user_password(self):
    #     """
    #     Test for updating business admin user password
    #     """

    #     data = {'old_password':"1234",'new_password':'new_password','new_password_confirm':'new_password'}
    #     response = self.client.put(f'/server_api/business-admin/update-password/{str(self.businessadmin1.admin_user_name)}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Password updated successfully")

    #     #missing data
    #     data = {'old_password':"password",'new_password':'new_password'}
    #     response = self.client.put(f'/server_api/business-admin/update-password/{str(self.businessadmin1.admin_user_name)}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Please provide new password")

    # def test_delete_business_admin_user(self):
    #     """
    #     Test delete business admin user
    #     """
    #     response = self.client.delete(f'/server_api/business-admin/delete/{str(self.businessadmin1.admin_user_name)}/')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Admin deleted successfully")

    # #test admin positions
    # def test_fetch_admin_positions(self):
    #     """
    #     Test for fetching admin postions
    #     """
    #     #all
    #     response = self.client.get(f'/server_api/business-admin/admin-position/fetch-positions/')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['admin_positions']),2)
    #     self.assertEqual(response.data['message'],"All Admin positions fetched successfully!")
    
    #     #name
    #     response = self.client.get(f'/server_api/business-admin/admin-position/fetch-positions/?name={self.adminposition1.name}')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     existing_data = serializers.AdminPositionSerializer(self.adminposition1).data
    #     returned_data = response.data['admin_positions']
    #     self.assertEqual(returned_data,existing_data)
    #     self.assertEqual(response.data['message'],"Admin position fetched successfully!")
    
    # def test_create_admin_position(self):
    #     """
    #     Test for creating admin position
    #     """

    #     data = {'name':'ppp'}
    #     response = self.client.post(f'/server_api/business-admin/admin-position/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"Admin position created successfully")

    #     #no name
    #     data = {}
    #     response = self.client.post(f'/server_api/business-admin/admin-position/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    # def test_update_admin_position(self):
    #     """
    #     Test for updating admin postion
    #     """
    #     data = {'name':'pppl','description':'okoko'}
    #     response = self.client.put(f'/server_api/business-admin/admin-position/update/{self.adminposition1.pk}/',data,format='json')
    #     self.assertEqual(response.data['message'],"Admin position successfully updated")
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)

    # def test_delete_admin_position(self):
    #     """
    #     Test delete admin postion
    #     """
    #     response = self.client.delete(f'/server_api/business-admin/admin-position/delete/{self.adminposition1.pk}/')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Admin position deleted successfully")

    # #product brands
    # def test_fetch_product_brand(self):
    #     """
    #     Test for creating product brand
    #     """
    #     #fetching all
    #     response = self.client.get(f'/server_api/product/product-brand/fetch-product-brands/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(len(response.data['product_brands']),2)
    #     expected_data = Product_Brands.objects.all()
    #     returned_data = response.data['product_brands']
    #     expected_data_serialized = product_serializers.Product_Brands_Serializer(expected_data, many=True).data
    #     self.assertEqual(returned_data, expected_data_serialized)

    #     #fetching single
    #     response = self.client.get(f'/server_api/product/product-brand/fetch-product-brands/?pk={self.product_brand1.pk}')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     expected_data = Product_Brands.objects.get(pk=self.product_brand1.pk)
    #     returned_data = response.data['product_brands']
    #     expected_data_serialized = product_serializers.Product_Brands_Serializer(expected_data, many=False).data
    #     self.assertEqual(returned_data, expected_data_serialized)

    #     #fetching using name
    #     response = self.client.get(f'/server_api/product/product-brand/fetch-product-brands/?brand_name={self.product_brand1.brand_name}')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     expected_data = Product_Brands.objects.get(pk=self.product_brand1.pk)
    #     returned_data = response.data['product_brands']
    #     expected_data_serialized = product_serializers.Product_Brands_Serializer(expected_data, many=False).data
    #     self.assertEqual(returned_data, expected_data_serialized)

    # def test_create_product_brand(self):
    #     """
    #     Test for creating product brand
    #     """
    #     data = {'brand_name':"simu",'brand_established_year':2008,'is_own_brand':True}
    #     response = self.client.post(f'/server_api/product/product-brand/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"Brand created")

    #     #duplicate
    #     data = {'brand_name':"Loreal",'brand_established_year':2008,'is_own_brand':True}
    #     response = self.client.post(f'/server_api/product/product-brand/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Same brand exists in Database!")

    # def test_update_product_brand(self):
    #     """
    #     Test for updating product brand
    #     """
    #     data = {'brand_name':self.product_brand1.brand_name,'brand_established_year':2010}
    #     response = self.client.put(f'/server_api/product/product-brand/update/{self.product_brand1.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"Brand updated")

    #     #same name
    #     data = {'brand_name':'Dove','brand_established_year':2010}
    #     response = self.client.put(f'/server_api/product/product-brand/update/{self.product_brand1.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Same brand already exists!")

    # def test_delete_product_brand(self):
    #     """
    #     Test for deleting product brand
    #     """
    #     response = self.client.delete(f'/server_api/product/product-brand/delete/{self.product_brand1.pk}/') 
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Product brand deleted successfully!")

    # #test product flavours
    # def test_fetch_product_flavours(self):
    #     """
    #     Test to fetch product flavours
    #     """
    #     #all fetch
    #     response = self.client.get(f'/server_api/product/product-flavour/fetch-product-flavour/')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['product_flavours_data']),2) 
    #     expected_data = Product_Flavours.objects.all()
    #     expected_data = product_serializers.Product_Flavour_Serializer(expected_data,many=True).data
    #     returned_data = response.data['product_flavours_data']
    #     self.assertEqual(returned_data,expected_data)

    #     #pk
    #     response = self.client.get(f'/server_api/product/product-flavour/fetch-product-flavour/?pk={self.product_flavour1.pk}')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(len(response.data),2) 
    #     expected_data = Product_Flavours.objects.get(pk=self.product_flavour1.pk)
    #     expected_data = product_serializers.Product_Flavour_Serializer(expected_data,many=False).data
    #     returned_data = response.data['product_flavours_data']
    #     self.assertEqual(returned_data,expected_data)

    # def test_create_product_flavour(self):
    #     """
    #     Test for creating product flavour
    #     """
    #     data = {'product_flavour_name':"anana"}
    #     response = self.client.post(f'/server_api/product/product-flavour/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"New Product flavour, anana successfully added!")

    #     #duplicate
    #     data = {'product_flavour_name':self.product_flavour2.product_flavour_name}
    #     response = self.client.post(f'/server_api/product/product-flavour/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Same flavour exists in Database!")

    # def test_update_product_flavour(self):
    #     """
    #     test for updating product flavour
    #     """

    #     data = {'product_flavour_pk':self.product_flavour1.pk,'product_flavour_name':"sami"}
    #     response = self.client.put(f'/server_api/product/product-flavour/update/{self.product_flavour1.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Product flavour updated successfully!")

    # def test_delete_product_flavour(self):
    #     """
    #     test for deleting product flavour
    #     """
    #     response = self.client.delete(f'/server_api/product/product-flavour/delete/{self.product_flavour1.pk}/')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Product flavour deleted successfully!")

    # #product tests
    # def test_fetch_product(self):
    #     """
    #     test for fetching product
    #     """        
    #     #all
    #     response = self.client.get(f'/server_api/product/fetch-product/')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     existing_data = Product.objects.all()
    #     existing_data = product_serializers.Product_Serializer(existing_data,many=True).data
    #     returned_data = response.data['product_data']
    #     self.assertEqual(existing_data,returned_data)
    #     #using category list
    #     response = self.client.get(f'/server_api/product/fetch-product/?product_category_pk_list={[self.product_category1.pk,self.product_category2.pk]}')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     existing_data = Product.objects.filter(Q(product_category = self.product_category1) | Q(product_category = self.product_category2))
    #     existing_data = product_serializers.Product_Serializer(existing_data,many=True).data
    #     returned_data = response.data['product_data']
    #     self.assertEqual(existing_data,returned_data)

    #     #using sub category list
    #     response = self.client.get(f'/server_api/product/fetch-product/?product_sub_category_pk_list={[self.product_sub_category1.pk,self.product_sub_category2.pk]}')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     existing_data = Product.objects.filter(Q(product_sub_category = self.product_sub_category1.pk) | Q(product_sub_category = self.product_sub_category2))
    #     existing_data = product_serializers.Product_Serializer(existing_data,many=True).data
    #     returned_data = response.data['product_data']
    #     self.assertEqual(existing_data,returned_data)

    # def test_create_product(self):
    #     """
    #     Test for creating product
    #     """
        
    #     data = {'product_name':"ooo",'product_category_pk_list':[self.product_category1.pk,self.product_category2.pk],
    #             'product_sub_category_pk_list' : [self.product_sub_category1.pk],'product_description':"pppp",
    #             'product_summary':"ppopop"
    #             }
    #     response = self.client.post(f'/server_api/product/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"Product, ooo created!")
        
    #     #duplicate
    #     data = {'product_name':"Dove Cleanser",'product_category_pk_list':[self.product_category1.pk,self.product_category2.pk],
    #             'product_sub_category_pk_list' : [self.product_sub_category1.pk],'product_description':"pppp",
    #             'product_summary':"ppopop"
    #             }
    #     response = self.client.post(f'/server_api/product/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Same product already exists!")

    # def test_update_product(self):
    #     """
    #     Test for updating product
    #     """
    #     data = {'product_pk':self.product1.pk,'product_name':"ooo",'product_category_pk_list':[self.product_category2.pk],
    #             'product_sub_category_pk_list' : [self.product_sub_category1.pk],'product_description':"pppp",
    #             'product_summary':"ppopop"
    #             }
    #     response = self.client.put(f'/server_api/product/update/{self.product1.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Product updated successfully!")

    #     #duplicate
    #     data = {'product_pk':self.product1.pk,'product_name':"Dove85 Cleanser",'product_category_pk_list':[self.product_category1.pk,self.product_category2.pk],
    #             'product_sub_category_pk_list' : [self.product_sub_category1.pk],'product_description':"pppp",
    #             'product_summary':"ppopop"
    #             }
    #     response = self.client.put(f'/server_api/product/update/{self.product1.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Same product name already exists!")

    # def test_delete_product(self):
    #     """
    #     Test delete product
    #     """
    #     response = self.client.delete(f'/server_api/product/delete/{self.product1.pk}/')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Product deleted successfully")

    # #prodcut sky
    # def test_fetch_product_sku(self):
    #     """
    #     Test fetch product sku fetch
    #     """
    #     #with pk
    #     response = self.client.get(f'/server_api/product/product-sku/fetch-product-sku/?pk={self.product_sku1.pk}')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Fetched successfully")

    #     #without
    #     response = self.client.get(f'/server_api/product/product-sku/fetch-product-sku/')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"No parameter passed! Must pass a single parameter")

    # def test_create_product_sku(self):
    #     """
    #     Test product sku creation
    #     """
    #     data = {'product_pk':self.product2.pk,'product_price':400,'product_stock':800,'product_size':'XXL',
    #             'product_flavours_pk_list':[self.product_flavour1.pk,self.product_flavour2.pk]}
    #     response = self.client.post(f'/server_api/product/product-sku/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"Product sku created successfully")

    # def test_update_product_sku(self):
    #     """
    #     Test for updating product sku
    #     """

    #     data = {'product_id':self.product2.pk,'product_price':400,'product_stock':800,'product_size':'XXL','product_color':'navy yellow',
    #             'product_flavours_pk_list':[self.product_flavour1.pk,self.product_flavour2.pk]}
    #     response = self.client.put(f'/server_api/product/product-sku/update/{self.product_sku2.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Product sku updated with new sku id")
        
    # def test_delete_product_sku(self):
    #     """
    #     Test for deleting product sku
    #     """
    #     response = self.client.delete(f'/server_api/product/product-sku/delete/{self.product_sku2.pk}/')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Product sku successfully deleted!")

    #     #delete again
    #     # response = self.client.delete(f'/server_api/product/product-sku/delete/{self.product_sku2.pk}/')
    #     # self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     # self.assertEqual(response.data['error'],"An unexpected error occurred while deleting product sku! Please try again later.")



#uncomment from up




    #product images
    # def test_fetch_product_images(self):
    #     """
    #     Test for fetching product images
    #     """
    #     #fetch all
    #     response = self.client.get(f'/server_api/product/product-images/fetch-product-image/')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"All product images fetched successfully")

    #     #using product_image_pk
    #     response = self.client.get(f'/server_api/product/product-images/fetch-product-image/?product_image_pk={self.product_image.pk}')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Product images fetched successfully")

    # def test_create_product_image(self):
    #     """
    #     Test for creating product images
    #     """

    #     image = ServerAPITestCases.generate_test_image('yellow',1)
    #     image2 = ServerAPITestCases.generate_test_image('green',2)
    #     data = {'product_image_list':[image,image2]}
    #     response = self.client.post(f'/server_api/product/product-images/create/{self.product1.pk}/',data,format='multipart')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"Product image created successfully")

    # def test_update_product_image(self):
    #     """
    #     Test for updating product image
    #     """

    #     image_old = ServerAPITestCases.generate_test_image('yellow',3)
    #     image_new = ServerAPITestCases.generate_test_image('pink',4)
    #     self.product_image.product_image = image_old
    #     data = {'new_image':image_new,'size':'XXL'}
    #     response = self.client.put(f'/server_api/product/product-image/update/{self.product_image.pk}/',data,format='multipart')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Product image updated successfully")

    # def test_delete_product_image(self):
    #     """
    #     Test for deleting product image
    #     """
        
    #     image_old = ServerAPITestCases.generate_test_image('yellow',3)
    #     self.product_image.product_image = image_old
    #     self.product_image.save()
    #     time.sleep(10)
    #     response = self.client.delete(f'/server_api/product/product-image/delete/{self.product_image.pk}/')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Product image deleted successfully")

    def test_fetch_product_discount(self):
        """
        Test for fetching product discount
        """
        #fetching all
        response = self.client.get(f'/server_api/product/product-discounts/fetch-product-discount/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data['product_discount']),3)
        self.assertEqual(response.data['message'],"All product discounts fetched successfully")
    
        #product_discount_pk
        response = self.client.get(f'/server_api/product/product-discounts/fetch-product-discount/?product_discount_pk={self.active_discount.pk}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Product Discount fetched successfully")

        #discount_name
        # response = self.client.get(f'/server_api/product/product-discounts/fetch-product-discount/?discount_name={self.inactive_discount.discount_name}')
        # self.assertEqual(response.status_code,status.HTTP_200_OK)
        # self.assertEqual(response.data['message'],"Product Discount fetched successfully")

        #is_active
        response = self.client.get(f'/server_api/product/product-discounts/fetch-product-discount/?is_active={True}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Active Product Discount fetched successfully")

        #category
        response = self.client.get(f'/server_api/product/product-discounts/fetch-product-discount/?product_id={self.product1.pk}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Product Discounts fetched successfully")

    def test_create_product_discount(self):
        """
        Test for creating product discount
        """

        data = {
            'discount_name': 'EWEWEW',
            'discount_amount': 500,
            'start_date': "2025-01-29T15:47:32.987654",
            'end_date': "2025-02-02T15:47:32.987654",
            'is_active':True,
            'product_id':self.product2.pk
        }
        response = self.client.post(f'/server_api/product/product-discounts/create/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"Product discount created successfully.")

    def test_update_product_discount(self):
        """
        Test for updating product discount
        """
        data = {
            'discount_name': 'EWEWEW85',
            'discount_amount': 500,
            'start_date': "2025-01-29T15:47:32.987654",
            'end_date': "2025-02-02T15:47:32.987654",
            'is_active':True,
            'product_id':self.product3.pk,
            'product_discount_product_id_pk':self.active_discount.product_id_pk
        }
        response = self.client.put(f'/server_api/product/product-discounts/update/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        print(response.data['message'])




#uncomment from down
    #business admin permission
    # def test_fetch_admin_permissions(self):
    #     """
    #     Test for fetching all permissions
    #     """

    #     response = self.client.get(f'/server_api/business-admin/admin-permissions/fetch-admin-permissions/')
    #     self.assertEqual(len(response.data['admin_permission']),3)
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    #     #using name
    #     response = self.client.get(f'/server_api/business-admin/admin-permissions/fetch-admin-permissions/?permission_name={self.admin_permission.permission_name}')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Permission fetched successfully")

    # def test_create_admin_permissions(self):
    #     """
    #     Test for creating admin permissions
    #     """
    #     data = {'permission_name':AdminPermissions.CREATE}
    #     response = self.client.post(f'/server_api/business-admin/admin-permissions/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    #     data = {'permission_name':AdminPermissions.DELETE}
    #     response = self.client.post(f'/server_api/business-admin/admin-permissions/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    # def test_update_admin_permissions(self):
    #     """
    #     Test for updating admin permissions
    #     """

    #     data = {'permission_name':AdminPermissions.CREATE,'permission_description':'newwewe'}
    #     response = self.client.put(f'/server_api/business-admin/admin-permissions/update/{self.admin_permission.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)

    #     data = {}
    #     response = self.client.put(f'/server_api/business-admin/admin-permissions/update/{self.admin_permission.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    # def test_delete_admin_permissions(self):
    #     """
    #     Test for deleting admin permissions
    #     """
    #     response = self.client.delete(f'/server_api/business-admin/admin-permissions/delete/{self.admin_permission.pk}/')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)


    #business admin position for user
    # def test_fetch_position_for_admin(self):
    #     """
    #     Test for fetching position for admin
    #     """
    #     data= {'admin_user_name':self.businessadmin1.admin_user_name}
    #     response = self.client.post(f'/server_api/business-admin/admin-position/fetch-position-for-admin/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Fetched successfully")

    # def test_add_postion_for_admin(self):
    #     """
    #     Test for adding position for admin
    #     """
    #     data= {'admin_user_name':self.businessadmin3.admin_user_name,'position_pk':self.adminposition1.pk}
    #     response = self.client.post(f'/server_api/business-admin/admin-position/add-position-for-admin/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"Successfully added")

    #     #existing
    #     data= {'admin_user_name':self.businessadmin1.admin_user_name,'position_pk':self.adminposition2.pk}
    #     response = self.client.post(f'/server_api/business-admin/admin-position/add-position-for-admin/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['error'],"Admin already has a role")
    
    # def test_update_position_for_admin(self):

    #     """
    #     Test for updating position for admin
    #     """
    #     data = {'admin_user_name':self.businessadmin1.admin_user_name,'position_pk':self.adminposition2.pk}
    #     response = self.client.put(f'/server_api/business-admin/admin-position/update-position-for-admin/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Successfully updated")
    
    # def test_delete_position_for_admin(self):
    #     """
    #     test for deleteing position for admin
    #     """
    #     data = {'admin_user_name':self.businessadmin1.admin_user_name}
    #     response = self.client.delete(f'/server_api/business-admin/admin-position/delete-position-for-admin/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Admin position removed successfully")

    # #admin role permission test
    # def test_fetch_admin_role_permissions(self):
    #     """
    #     Test for fetching admin role permissions
    #     """
    #     #all
    #     response = self.client.get(f'/server_api/business-admin/admin-role-permission/fetch-role-permissions/')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"All fetched successfully")
    #     self.assertEqual(len(response.data['admin_role_permission']),2)

    #     #using pk
    #     response = self.client.get(f'/server_api/business-admin/admin-role-permission/fetch-role-permissions/?admin_role_permission_pk={self.admin_role_permission1.pk}')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Fetched successfully")

    # def test_create_admin_role_permissions(self):
    #     """
    #     Test for creating admin role permissions
    #     """

    #     data = {'admin_position_pk':self.adminposition1.pk,'admin_permission_pk_list':[self.admin_permission.pk,self.admin_permission2.pk]}
    #     response = self.client.post(f'/server_api/business-admin/admin-role-permission/create/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'],"Created successfully")

    # def test_update_admin_role_permissions(self):

    #     """
    #     Test for updating admin role permissions
    #     """
    #     data = {'admin_permission_pk_list':[self.admin_permission2.pk]}
    #     response = self.client.put(f'/server_api/business-admin/admin-role-permission/update/{self.adminposition1.pk}/',data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'],"Updated successfully")

    # def test_delete_admin_role_permissions(self):
    #     """
    #     Test for deleting admin role permissions
    #     """
    #     response = self.client.delete(f'/server_api/business-admin/admin-role-permission/delete/{self.adminposition1.pk}/')
    #     self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data['message'],"Deleted successfully")

    #test for fetching product with discounts and sku
    def test_fetch_product_with_discounts_and_sku(self):
        """
        Test for fetching products with discount and skus
        """
        response = self.client.get(f'/server_api/product/fetch-product-details/?product_pk={self.product1.pk}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Fetched successfully")

    def test_fetch_user_notifications(self):

        data={
            'user_name':self.user.username
        }
        response = self.client.get('/server_api/system/notification/fetch/',data=data,format='json')
        # print(response.data)

    #orders

    def test_fetch_order_details(self):

        response = self.client.get(f'/server_api/order/fetch/?user_name={self.customer1.username}')
        # print(response.data)

        #orderid
        response = self.client.get(f'/server_api/order/fetch/?order_id={self.order3.order_id}')
        # print(response.data)

        #all
        response = self.client.get(f'/server_api/order/fetch/')
        # print(response.data)
    
    def test_update_order_details(self):
        
        data = {
            'delivery_time_pk':self.delivery_time3.pk
        }
        response = self.client.put(f'/server_api/order/update-details/{self.order1.order_id}/',data=data,format='json')
        self.assertEqual(response.data['message'],"Updated Sucessfully")


    










    

