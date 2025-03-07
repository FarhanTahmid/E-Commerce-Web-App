from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.core.files.base import ContentFile
from orders.models import Order, OrderDetails, OrderShippingAddress, OrderPayment, Invoice
from products.models import Product, Product_SKU
from customer.models import Accounts
from orders.invoice_generator import InvoiceGenerator
from system.models import *
import json
import tempfile
from io import BytesIO
from zipfile import ZipFile

User = get_user_model()

class InvoiceAPITestBase(TestCase):
    """Base test class with common setup for invoice tests"""
    
    def setUp(self):
        # Create test users
        self.customer = User.objects.create_user(
            email='customer@example.com',
            username='customer',
            password='testpass123',
        )
        
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123',
        )
        
        # Create test products
        self.product = Product.objects.create(
            product_name="Test Product",
            product_description="Test Description"
        )
        
        # Create SKU
        self.sku = Product_SKU.objects.create(
            product_id=self.product,
            product_sku="SKU001",
            product_price=100.00,
            product_stock=10
        )
        
        # Create order
        self.order = Order.objects.create(
            order_id="ORD12345",
            customer_id=self.customer,
            total_amount=100.00,
            order_status='confirmed'
        )
        
        # Create order details
        self.order_details = OrderDetails.objects.create(
            order_id=self.order,
            product_sku=self.sku,
            quantity=1,
            units=1,
            subtotal=100.00
        )
        
        # Create shipping address
        self.shipping_address = OrderShippingAddress.objects.create(
            order_id=self.order,
            address_line1="123 Test St",
            city="Test City",
            country="Test Country",
            postal_code="12345"
        )
        
        # Create payment details
        self.payment = OrderPayment.objects.create(
            order_id=self.order,
            payment_mode='credit_card',
            payment_status='success',
            payment_amount=100.00,
            payment_reference="PAY12345"
        )
        
        # Create another order for a different status
        self.delivered_order = Order.objects.create(
            order_id="ORD67890",
            customer_id=self.customer,
            total_amount=200.00,
            order_status='delivered'
        )
        
        OrderDetails.objects.create(
            order_id=self.delivered_order,
            product_sku=self.sku,
            quantity=2,
            units=1,
            subtotal=200.00
        )
        
        OrderShippingAddress.objects.create(
            order_id=self.delivered_order,
            address_line1="123 Test St",
            city="Test City",
            country="Test Country",
            postal_code="12345"
        )
        
        OrderPayment.objects.create(
            order_id=self.delivered_order,
            payment_mode='credit_card',
            payment_status='success',
            payment_amount=200.00,
            payment_reference="PAY67890"
        )
        
        # Create invoices
        self.invoice = Invoice.objects.create(
            order=self.order,
            invoice_number=f"INV-{timezone.now().strftime('%Y%m%d')}-{self.order.pk}",
            is_finalized=True
        )
        
        # Add sample invoice file content
        self.invoice.invoice_file.save(
            f"Invoice_{self.invoice.invoice_number}.pdf", 
            ContentFile(b"Test PDF content"), 
            save=True
        )
        
        self.delivered_invoice = Invoice.objects.create(
            order=self.delivered_order,
            invoice_number=f"INV-{timezone.now().strftime('%Y%m%d')}-{self.delivered_order.pk}",
            is_finalized=True
        )
        
        self.delivered_invoice.invoice_file.save(
            f"Invoice_{self.delivered_invoice.invoice_number}.pdf", 
            ContentFile(b"Test delivered PDF content"), 
            save=True
        )
        
        # Setup API client
        self.client = APIClient()
    
    def get_customer_auth(self):
        """Get customer auth token and set credentials"""
        refresh = RefreshToken.for_user(self.customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def get_admin_auth(self):
        """Get admin auth token and set credentials"""
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

class UserInvoiceAPITests(InvoiceAPITestBase):
    """Test customer-facing invoice API endpoints"""
    
    def test_user_invoice_download(self):
        """Test customer downloading their own invoice"""
        self.get_customer_auth()
        response = self.client.get(f'/customer-order/{self.order.order_id}/invoice/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue('attachment; filename=' in response['Content-Disposition'])
  