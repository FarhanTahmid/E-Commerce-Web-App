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
        response = self.client.get(f'/client_api/customer-order/{self.order.order_id}/invoice/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue('attachment; filename=' in response['Content-Disposition'])
    
    def test_user_cannot_access_other_customer_invoice(self):
        """Test customer cannot access another customer's invoice"""
        # Create another customer
        other_customer = User.objects.create_user(
            email='other@example.com',
            username='other',
            password='testpass123'
        )
        
        # Create an order for the other customer
        other_order = Order.objects.create(
            order_id="ORD-OTHER",
            customer_id=other_customer,
            total_amount=100.00,
            order_status='confirmed'
        )
        
        # Login as main customer
        self.get_customer_auth()
        
        # Try to access other customer's invoice
        response = self.client.get(f'/client_api/customer-order/{other_order.order_id}/invoice/')
        
        # Should be forbidden
        self.assertEqual(response.status_code, 404)
    
    # def test_invoice_list(self):
    #     """Test customer listing their invoices"""
    #     self.get_customer_auth()
    #     response = self.client.get(f'/client_api/customer-order/invoices/')
        
    #     self.assertEqual(response.status_code, 200)
    #     data = response.json()
        
    #     # Should have 2 invoices
    #     self.assertEqual(data['total_invoices'], 2)
    #     self.assertEqual(len(data['invoices']), 2)
        
    #     # Verify invoice data structure
    #     invoice = data['invoices'][0]
    #     self.assertIn('invoice_number', invoice)
    #     self.assertIn('order_id', invoice)
    #     self.assertIn('total_amount', invoice)
    #     self.assertIn('download_url', invoice)
    def test_unauthenticated_access(self):
        """Test unauthenticated access is denied"""
        # Clear credentials
        self.client.credentials()
        
        # Try to access invoice endpoints
        response = self.client.get(f'/client_api/customer-order/{self.order.order_id}/invoice/')
        self.assertEqual(response.status_code, 401)
        
        response = self.client.get('/client_api/customer-order/invoices/')
        self.assertEqual(response.status_code, 401)

class AdminInvoiceAPITests(InvoiceAPITestBase):
    """Test admin-facing invoice API endpoints"""
    
    def test_admin_invoice_list(self):
        """Test admin listing all invoices"""
        self.get_admin_auth()
        response = self.client.get('/server_api/invoices/')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have pagination data
        self.assertIn('pagination', data)
        self.assertIn('invoices', data)
        
        # Should have our 2 test invoices
        self.assertEqual(len(data['invoices']), 2)
    
    def test_admin_invoice_filtering(self):
        """Test admin filtering invoices"""
        self.get_admin_auth()
        
        # Filter by order status
        response = self.client.get('/server_api/invoices/?status=delivered')
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['invoices']), 1)
        self.assertEqual(data['invoices'][0]['order_status'], 'delivered')
        
        # Filter by customer
        response = self.client.get(f'/server_api/invoices/?customer_id={self.customer.id}')
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['invoices']), 2)
    
    def test_admin_invoice_download(self):
        """Test admin downloading an invoice"""
        self.get_admin_auth()
        response = self.client.get(f'/server_api/invoices/{self.invoice.id}/download/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
    
    def test_admin_bulk_invoice_download(self):
        """Test admin downloading multiple invoices as ZIP"""
        self.get_admin_auth()
        
        # Request both test invoices
        invoice_ids = [self.invoice.id, self.delivered_invoice.id]
        response = self.client.post(
            '/server_api/invoices/bulk-download/',
            {'invoice_ids': invoice_ids},
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        
        # Verify ZIP file contains expected files
        with tempfile.TemporaryFile() as temp_file:
            temp_file.write(response.content)
            temp_file.seek(0)
            
            with ZipFile(temp_file, 'r') as zip_file:
                file_list = zip_file.namelist()
                self.assertEqual(len(file_list), 2)
    
    def test_admin_customer_invoices(self):
        """Test admin viewing invoices for a specific customer"""
        self.get_admin_auth()
        response = self.client.get(f'/server_api/customers/{self.customer.id}/invoices/')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have customer data and invoices
        self.assertIn('customer', data)
        self.assertIn('invoices', data)
        self.assertEqual(data['customer']['id'], self.customer.id)
        self.assertEqual(len(data['invoices']), 2)
    
    def test_admin_generate_invoice(self):
        """Test admin generating an invoice for an order"""
        self.get_admin_auth()
        
        # Create new order without invoice
        new_order = Order.objects.create(
            order_id="ORD-NEW",
            customer_id=self.customer,
            total_amount=300.00,
            order_status='confirmed'
        )
        
        OrderDetails.objects.create(
            order_id=new_order,
            product_sku=self.sku,
            quantity=3,
            units=1,
            subtotal=300.00
        )
        
        OrderShippingAddress.objects.create(
            order_id=new_order,
            address_line1="123 Test St",
            city="Test City",
            country="Test Country",
            postal_code="12345"
        )
        
        OrderPayment.objects.create(
            order_id=new_order,
            payment_mode='credit_card',
            payment_status='success',
            payment_amount=300.00,
            payment_reference="PAY-NEW"
        )
        
        # Generate invoice
        response = self.client.post(f'/server_api/orders/{new_order.order_id}/generate-invoice/')
        
        # Check ErrorLogs for any logged errors
        recent_errors = ErrorLogs.objects.all().order_by('-timestamp')[:5]
        for error in recent_errors:
            print(f"Error type: {error.error_type}")
            print(f"Error message: {error.error_message}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Verify invoice was created in database
        self.assertTrue(Invoice.objects.filter(order=new_order).exists())
    
    # def test_customer_cannot_access_admin_endpoints(self):
    #     """Test customers cannot access admin endpoints"""
    #     self.get_customer_auth()
        
    #     # Try to access admin endpoints
    #     response = self.client.get('/server_api/invoices/')
    #     self.assertEqual(response.status_code, 403)
        
    #     response = self.client.get(f'/server_api/invoices/{self.invoice.id}/download/')
    #     self.assertEqual(response.status_code, 403)
        
    #     response = self.client.post('/server_api/invoices/bulk-download/', {'invoice_ids': [1]}, format='json')
    #     self.assertEqual(response.status_code, 403)
    
class InvoiceGenerationTest(InvoiceAPITestBase):
    """Test invoice generation functionality"""
    
    def test_invoice_pdf_generation(self):
        """Test PDF invoice generation"""
        pdf_data = InvoiceGenerator.generate_pdf_invoice(self.order)
        self.assertIsNotNone(pdf_data)
        self.assertTrue(isinstance(pdf_data, bytes))
    
    def test_invoice_html_generation(self):
        """Test HTML invoice generation"""
        html_content = InvoiceGenerator.generate_html_invoice(self.order)
        self.assertIsNotNone(html_content)
        self.assertTrue(isinstance(html_content, str))
        self.assertTrue('<html' in html_content)
    
    def test_invoice_context_for_paid_order(self):
        """Test context for paid order has PAID flag"""
        self.order.order_status = 'shipped'
        self.order.save()
        
        context = InvoiceGenerator.get_invoice_context(self.order)
        self.assertTrue(context['is_paid'])
        self.assertFalse(context['is_cancelled'])
    
    def test_invoice_context_for_cancelled_order(self):
        """Test context for cancelled order has CANCELLED flag"""
        self.order.order_status = 'cancelled'
        self.order.save()
        
        context = InvoiceGenerator.get_invoice_context(self.order)
        self.assertFalse(context['is_paid'])
        self.assertTrue(context['is_cancelled'])