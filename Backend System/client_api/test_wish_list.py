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
from system.models import NotificationTo

now = timezone.now()
User = get_user_model()

class WishListAPITests(TestCase):

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
        
        self.client = APIClient()
        
    def get_auth_header(self, user):
        token = AccessToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    def test_create_or_fetch_wish_list(self):

        response = self.client.post('/client_api/customer-wishlist/create_or_fetch/')
        self.assertEqual(response.status_code, 201)
        wish_list_id = response.data['id']
        print(response.data)
        
        # Test fetching existing wishlist
        response = self.client.post('/client_api/customer-wishlist/create_or_fetch/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], wish_list_id)

    def test_create_or_fetch_authenticated(self):
        # Create user cart
        headers = self.get_auth_header(self.user1)  # Already a dict, e.g. {'HTTP_AUTHORIZATION': 'Bearer <token>'}
        # Pass it directly
        self.client.credentials(**headers)
        response = self.client.post('/client_api/customer-wishlist/create_or_fetch/')
        self.assertEqual(response.status_code, 201)

    def test_wish_list_merging(self):
        # Simulate guest session
        guest_ip = '192.168.1.100'
        
        # Create guest wish list
        guest_response = self.client.post(
            '/client_api/customer-wishlist/create_or_fetch/',
            HTTP_X_FORWARDED_FOR=guest_ip
        )
        self.assertEqual(guest_response.status_code, 201)
        guest_wish_list_id = guest_response.data['id']
     
        
        # Add item to guest wish list
        WishlistItem.objects.create(
            wishlist=Wishlist.objects.get(pk=guest_wish_list_id),
            product_sku=self.sku1,
        )

        # Authenticate user and trigger merge
        headers = self.get_auth_header(self.user1)
        user_response = self.client.post(
            '/client_api/customer-wishlist/create_or_fetch/',
            HTTP_X_FORWARDED_FOR=guest_ip,  # Same IP!
            **headers
        )
        
        # Verify successful merge
        self.assertEqual(user_response.status_code, 200)
        
        # Check merged wish list contents
        wishlist_cart = Wishlist.objects.get(customer_id=self.user1)
        # self.assertEqual(wishlist_cart.product_sku, self.sku1)
        
        # Ensure guest cart was cleaned up
        self.assertFalse(Wishlist.objects.filter(id=guest_wish_list_id).exists())

    def test_add_product_authenticated_to_wishlist(self):
        # Setup
        headers = self.get_auth_header(self.user1)
        fetch_cart_response=self.client.post('/client_api/customer-wishlist/create_or_fetch/', **headers)
        self.assertEqual(fetch_cart_response.status_code, 201)
        wish_list_data=fetch_cart_response.data
        wish_list_id= wish_list_data['id']
        
        # Now add product to the cart
        add_url = f'/client_api/customer-wishlist/{wish_list_id}/add_product/'
        headers = self.get_auth_header(self.user1)
        payload = {'sku_id': self.sku1.id}

        response = self.client.post(add_url, payload, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(WishlistItem.objects.count(), 1, "Wishlist Items should have 1 item after adding.")
        wish_list_item = WishlistItem.objects.first()
        self.assertEqual(wish_list_item.product_sku, self.sku1)
        
    def test_add_product_t0o_wishlist_as_guest(self):
        # Create guest cart
        response = self.client.post('/client_api/customer-wishlist/create_or_fetch/')
        self.assertEqual(response.status_code, 201)
        wish_list_id = response.data['id']
        
        # Add product to guest cart
        add_url = f'/client_api/customer-wishlist/{wish_list_id}/add_product/'
        payload = {'sku_id': self.sku1.id}

        # Simulate the same IP so the user can access the cart
        response = self.client.post(add_url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(WishlistItem.objects.count(), 1, "Guest wish list should have 1 item added.")

    def test_remove_item(self):
        # Setup
        fetch_response = self.client.post('/client_api/customer-wishlist/create_or_fetch/')
        self.assertEqual(fetch_response.status_code, 201)
        wish_list_id = fetch_response.data['id']
        
        # Add product to guest cart
        add_url = f'/client_api/customer-wishlist/{wish_list_id}/add_product/'
        payload = {'sku_id': self.sku1.id}
        
        add_response = self.client.post(add_url, payload)
        self.assertEqual(add_response.status_code, 200)
                
        # Remove the item
        item_id = WishlistItem.objects.first().id
        remove_url = f'/client_api/customer-wishlist/{wish_list_id}/remove_item/?item_id={item_id}'
        response = self.client.delete(remove_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(WishlistItem.objects.count(), 0, "Wishlist should have 0 items after removal.")


