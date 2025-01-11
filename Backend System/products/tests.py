from django.test import TestCase
from products.models import *
from products.product_management import ManageProducts
from unittest import mock
from django.db import *
from system.models import *
# Create your tests here.

class TestManageProducts(TestCase):
    
    def setUp(self):
        # create sample data
        Product_type.objects.create(type="Cosmetics",description="Daily Life Product")
        Product_type.objects.create(type="Clothing",description="Daily Life Product")
        Product_type.objects.create(type="Groceries",description="Daily Life Product")
    
    def test_fetch_all_product_types_success(self):
        """
        Test if the function fetches all product types successfully.
        """
        product_types, message = ManageProducts.fetch_all_product_types()
        self.assertIsNotNone(product_types, "Product types should not be None.")
        self.assertEqual(product_types.count(), 3, "The function did not return all product types.")
        self.assertEqual(message, "Fetched all product types successfully!", "Success message is incorrect.")

    
    @mock.patch('products.models.Product_type.objects.all', side_effect=DatabaseError("Database Error"))
    def test_fetch_all_product_types_database_error(self, mock_all):
        """
        Test if the function handles DatabaseError correctly.
        """
        product_types, message = ManageProducts.fetch_all_product_types()
        self.assertIsNone(product_types, "Product types should be None on DatabaseError.")
        
    @mock.patch('products.models.Product_type.objects.all', side_effect=OperationalError("Operational Error"))
    def test_fetch_all_product_types_operational_error(self, mock_all):
        """
        Test if the function handles OperationalError correctly.
        """
        product_types, message = ManageProducts.fetch_all_product_types()
        self.assertIsNone(product_types, "Product types should be None on OperationalError.")
        
    @mock.patch('products.models.Product_type.objects.all', side_effect=ProgrammingError("Programming Error"))
    def test_fetch_all_product_types_programming_error(self, mock_all):
        """
        Test if the function handles ProgrammingError correctly.
        """
        product_types, message = ManageProducts.fetch_all_product_types()
        self.assertIsNone(product_types, "Product types should be None on ProgrammingError.")
        
    @mock.patch('products.models.Product_type.objects.all', side_effect=IntegrityError("Integrity Error"))
    def test_fetch_all_product_types_integrity_error(self, mock_all):
        """
        Test if the function handles IntegrityError correctly.
        """
        product_types, message = ManageProducts.fetch_all_product_types()
        self.assertIsNone(product_types, "Product types should be None on IntegrityError.")

    @mock.patch('products.models.Product_type.objects.all', side_effect=Exception("Unexpected Error"))
    def test_fetch_all_product_types_unexpected_error(self, mock_all):
        """
        Test if the function handles unexpected exceptions correctly.
        """
        product_types, message = ManageProducts.fetch_all_product_types()
        self.assertIsNone(product_types, "Product types should be None on an unexpected error.")
    
    
    def test_create_new_product_type_success(self):
        """
        Test creating a new product type successfully.
        """
        success, message = ManageProducts.create_product_type("Furnitures", "Furniture goods")
        self.assertTrue(success, "The function should return True on successful creation.")
        self.assertEqual(message, "New Product type Furnitures successfully added!",
                         "The success message is incorrect.")
        self.assertEqual(Product_type.objects.filter(type="Furnitures").count(), 1,
                         "The new product type should be added to the database.")

    def test_create_duplicate_product_type(self):
        """
        Test creating a product type that already exists.
        """
        success, message = ManageProducts.create_product_type("cosmEtiCs", "Duplicate electronic items")
        self.assertFalse(success, "The function should return False for duplicate types.")
        self.assertEqual(message, "Same type exists in Database!",
                         "The duplicate type message is incorrect.")
        self.assertEqual(Product_type.objects.filter(type="cosmEtiCs").count(), 0,
                         "No duplicate entries should be created in the database.")
    
    @mock.patch('products.models.Product_type.objects.create', side_effect=DatabaseError("Database Error"))
    def test_create_product_type_database_error(self, mock_create):
        """
        Test handling of a DatabaseError during product type creation.
        """
        success, message = ManageProducts.create_product_type("Toys", "Toys and games")
        self.assertFalse(success, "The function should return False on a DatabaseError.")
        
        self.assertEqual(ErrorLogs.objects.filter(error_type="DatabaseError").count(), 1,
                         "A DatabaseError should be logged in the ErrorLogs model.")