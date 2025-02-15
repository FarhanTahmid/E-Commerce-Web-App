from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from orders.models import Cart, CartItems,Product_SKU
from products.models import *
from orders.models import *
import json
from django.utils import timezone
from customer.models import *
import datetime
from .api_view_orders import generate_order_id
from rest_framework import status

now = timezone.now()
User = get_user_model()

class OrderAPITests(TestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            username='user2',
            password='testpass123'
        )
        
        self.address1 = CustomerAddress.objects.create(
            customer_id=self.user1,
            address_title = "Asylum",
            address_line1 = 'House-69',
            country = "USA",
            city = "DK",
            postal_code = '1216',
            created_at = now    
        )

        self.address2 = CustomerAddress.objects.create(
            customer_id=self.user2,
            address_title = "Asylum",
            address_line1 = 'House-69',
            country = "USA",
            city = "DK",
            postal_code = '1216',
            created_at = now    
        )

        # Create test products
        self.product1 = Product.objects.create(
            product_name="Test Product 1",
            product_description="Test Description 1"
        )
        self.product2 = Product.objects.create(
            product_name="Test Product 2",
            product_description="Test Description 2"
        )
        
        # Create SKUs
        self.sku1 = Product_SKU.objects.create(
            product_id=self.product1,
            product_sku="SKU001",
            product_price=100.00,
            product_stock=10
        )
        self.sku2 = Product_SKU.objects.create(
            product_id=self.product2,
            product_sku="SKU002",
            product_price=200.00,
            product_stock=5
        )

        self.cart1 = Cart.objects.create(
            customer_id = self.user1,
            cart_total_amount=1000,
            created_at = now
        )

        self.cart2 = Cart.objects.create(
            customer_id = self.user2,
            cart_total_amount=2000,
            created_at = now
        )

        self.cart_items1 = CartItems.objects.create(
            cart_id = self.cart1,
            product_sku = self.sku1,
            quantity = 3,
            created_at = now
        )

        self.cart_items2 = CartItems.objects.create(
            cart_id = self.cart2,
            product_sku = self.sku2,
            quantity = 3,
            created_at = now
        )

        self.coupon1 = Coupon.objects.create(
            coupon_code = 'UNIQUE1',
            discount_type = Coupon.DISCOUNT_TYPE_CHOICES[0][0],#percentage
            discount_percentage=30,
            maximum_discount_amount=100,
            start_date = now,
            end_date = now + datetime.timedelta(days=10),
            customer_id = self.user1,
            created_at = now

        )

        self.coupon2 = Coupon.objects.create(
            coupon_code = 'UNIQUE2',
            discount_type = Coupon.DISCOUNT_TYPE_CHOICES[1][1],#fixed
            discount_amount=50,
            usage_limit=1,
            maximum_discount_amount=100,
            start_date = now + datetime.timedelta(days=-5),
            end_date = now + datetime.timedelta(days=20),
            customer_id = self.user2,
            created_at = now

        )

        self.order1 = Order.objects.create(
            order_id = generate_order_id(self.user1.username,self.cart1.pk),
            customer_id = self.user1,
            order_date = now,
            total_amount = 5000,
            order_status = Order.ORDER_STATUS_CHOICES[0][0],#pending
            created_at = now

        )

        self.order2 = Order.objects.create(
            order_id = generate_order_id(self.user2.username,self.cart2.pk),
            customer_id = self.user2,
            order_date = now,
            total_amount = 5000,
            order_status = Order.ORDER_STATUS_CHOICES[0][0],#pending
            created_at = now

        )
        
        self.client = APIClient()
        
    def get_auth_header(self, user):
        token = AccessToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    def test_create_order(self):
        #test for creating order

        data = {
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001"
            },
            "payment_mode": "credit_card",
            'coupon_code':'UNIQUE1',
            'save_address':True
            }
        headers = self.get_auth_header(self.user1) 
        self.client.credentials(**headers)
        response = self.client.post('/client_api/customer-order/checkout/',data=data,format='json',headers=headers)
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        #with save address
        # data = {
        #     "use_saved_address":True,
        #     "payment_mode": "credit_card",
        #     'coupon_code':'UNIQUE2'
        #     }
        # headers = self.get_auth_header(self.user2) 
        # self.client.credentials(**headers)
        # response = self.client.post('/client_api/customer-order/checkout/',data=data,format='json',headers=headers)
        # self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # data = {
        #     'save_address':True,
        #     "shipping_address": {
        #         "street": "123 Main St",
        #         "city": "New York",
        #         "state": "NY",
        #         "zip_code": "10001"
        #     },
        #     "payment_mode": "credit_card"
        #     }
        # headers = self.get_auth_header(self.user1) 
        # self.client.credentials(**headers)
        # response = self.client.post('/client_api/customer-order/checkout/',data=data,format='json',headers=headers)
        # self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        
    
    