from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from orders.models import Cart, CartItems,Product_SKU
from products.models import Product
import json

User = get_user_model()

class CartAPITests(TestCase):
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
    
    def test_create_or_fetch_cart_guest(self):
        # Test guest cart creation
        response = self.client.post('/client_api/customer-cart/create_or_fetch/')
        self.assertEqual(response.status_code, 201)
        cart_id = response.data['id']
        
        # Test fetching existing guest cart
        response = self.client.post('/client_api/customer-cart/create_or_fetch/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], cart_id)
        
    def test_create_or_fetch_authenticated(self):
        # Create user cart
        headers = self.get_auth_header(self.user1)  # Already a dict, e.g. {'HTTP_AUTHORIZATION': 'Bearer <token>'}
        # Pass it directly
        self.client.credentials(**headers)
        response = self.client.post('/client_api/customer-cart/create_or_fetch/')
        self.assertEqual(response.status_code, 201)

        
    def test_cart_merging(self):
        # Simulate guest session
        guest_ip = '192.168.1.100'
        
        # Create guest cart
        guest_response = self.client.post(
            '/client_api/customer-cart/create_or_fetch/',
            HTTP_X_FORWARDED_FOR=guest_ip
        )
        self.assertEqual(guest_response.status_code, 201)
        guest_cart_id = guest_response.data['id']
        
        # Add item to guest cart
        CartItems.objects.create(
            cart_id_id=guest_cart_id,
            product_sku=self.sku1,
            quantity=2
        )

        # Authenticate user and trigger merge
        headers = self.get_auth_header(self.user1)
        user_response = self.client.post(
            '/client_api/customer-cart/create_or_fetch/',
            HTTP_X_FORWARDED_FOR=guest_ip,  # Same IP!
            **headers
        )
        
        # Verify successful merge
        self.assertEqual(user_response.status_code, 200)
        
        # Check merged cart contents
        user_cart = Cart.objects.get(customer_id=self.user1)
        self.assertEqual(user_cart.cartitems_set.count(), 1)
        
        # Ensure guest cart was cleaned up
        self.assertFalse(Cart.objects.filter(id=guest_cart_id).exists())
        
    def test_add_product_authenticated(self):
        # Setup
        headers = self.get_auth_header(self.user1)
        fetch_cart_response=self.client.post('/client_api/customer-cart/create_or_fetch/', **headers)
        self.assertEqual(fetch_cart_response.status_code, 201)
        cart_data=fetch_cart_response.data
        cart_id=cart_data['id']
        
        # Now add product to the cart
        add_url = f'/client_api/customer-cart/{cart_id}/add_product/'
        headers = self.get_auth_header(self.user1)
        payload = {'sku_id': self.sku1.id, 'quantity': 3}

        response = self.client.post(add_url, payload, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItems.objects.count(), 1, "Cart should have 1 item after adding.")
        cart_item = CartItems.objects.first()
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(cart_item.product_sku, self.sku1)
        
    def test_add_product_guest(self):
        # Create guest cart
        response = self.client.post('/client_api/customer-cart/create_or_fetch/')
        self.assertEqual(response.status_code, 201)
        cart_id = response.data['id']
        
        # Add product to guest cart
        add_url = f'/client_api/customer-cart/{cart_id}/add_product/'
        payload = {'sku_id': self.sku1.id, 'quantity': 2}

        # Simulate the same IP so the user can access the cart
        response = self.client.post(add_url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItems.objects.count(), 1, "Guest cart should have 1 item added.")
        cart_item = CartItems.objects.first()
        self.assertEqual(cart_item.quantity, 2)
        
    def test_update_item(self):
        # Setup
        fetch_response = self.client.post('/client_api/customer-cart/create_or_fetch/')
        self.assertEqual(fetch_response.status_code, 201)
        cart_id = fetch_response.data['id']
        
        # Add product to guest cart
        add_url = f'/client_api/customer-cart/{cart_id}/add_product/'
        payload = {'sku_id': self.sku1.id, 'quantity': 2}
        
        add_response = self.client.post(add_url, payload)
        self.assertEqual(add_response.status_code, 200)

        # Grab the item ID
        item_id = CartItems.objects.first().id

        # Update item quantity
        update_url = f'/client_api/customer-cart/{cart_id}/update_item/'
        response = self.client.put(
            update_url,
            {'item_id': item_id, 'quantity': 5}
            )
        self.assertEqual(response.status_code, 200)
        item = CartItems.objects.get(id=item_id)
        self.assertEqual(item.quantity, 5, "Item quantity should be updated to 5.")
        
    def test_remove_item(self):
        # Setup
        fetch_response = self.client.post('/client_api/customer-cart/create_or_fetch/')
        self.assertEqual(fetch_response.status_code, 201)
        cart_id = fetch_response.data['id']
        
        # Add product to guest cart
        add_url = f'/client_api/customer-cart/{cart_id}/add_product/'
        payload = {'sku_id': self.sku1.id, 'quantity': 2}
        
        add_response = self.client.post(add_url, payload)
        self.assertEqual(add_response.status_code, 200)
                
        # Remove the item
        item_id = CartItems.objects.first().id
        remove_url = f'/client_api/customer-cart/{cart_id}/remove_item/?item_id={item_id}'
        response = self.client.delete(remove_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItems.objects.count(), 0, "Cart should have 0 items after removal.")

        
    def test_clear_cart(self):
        # Setup
        fetch_response = self.client.post('/client_api/customer-cart/create_or_fetch/')
        self.assertEqual(fetch_response.status_code, 201)
        cart_id = fetch_response.data['id']
        
        add_url = f'/client_api/customer-cart/{cart_id}/add_product/'
        # Add two different products
        self.client.post(add_url, {'sku_id': self.sku1.id, 'quantity': 2})
        self.client.post(add_url, {'sku_id': self.sku2.id, 'quantity': 1})
        self.assertEqual(CartItems.objects.count(), 2, "Cart should have 2 items initially.")

        # Clear the cart
        clear_url = f'/client_api/customer-cart/{cart_id}/clear_cart/'
        response = self.client.delete(clear_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItems.objects.count(), 0, "Cart should be empty after clearing.")

        
    def test_stock_validation(self):
        # Setup
        fetch_response = self.client.post('/client_api/customer-cart/create_or_fetch/')
        self.assertEqual(fetch_response.status_code, 201)
        cart_id = fetch_response.data['id']
        
        add_url = f'/client_api/customer-cart/{cart_id}/add_product/'
        
        # Try exceeding the stock
        response = self.client.post(
            add_url,
            {'sku_id': self.sku1.id, 'quantity': 9999},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Insufficient stock', str(response.data))
        
    def test_cart_ownership(self):
        # user1 setup
        headers1 = self.get_auth_header(self.user1)
        self.client.credentials(**headers1)
        response = self.client.post('/client_api/customer-cart/create_or_fetch/')
        user1_cart_id = response.data.get('id')
        self.assertEqual(response.status_code, 201)

        # Switch to user2
        headers2 = self.get_auth_header(self.user2)
        self.client.credentials(**headers2)
        add_url = f'/client_api/customer-cart/{user1_cart_id}/add_product/'
        response = self.client.post(add_url, {'sku_id': self.sku1.id})
        self.assertEqual(response.status_code, 403)
