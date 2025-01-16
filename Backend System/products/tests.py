from django.test import TestCase
from django.utils import timezone
from products.models import *
from products.product_management import ManageProducts
from unittest import mock
from django.db import *
from system.models import *
# Create your tests here.

class TestManageProductsCategories(TestCase):
    
    def setUp(self):
        # create sample data with timezone-aware datetime
        now = timezone.now()
        Product_Category.objects.create(category_name="Cosmetics", description="Daily Life Product", created_at=now)
        Product_Category.objects.create(category_name="Clothing", description="Daily Life Product", created_at=now)
        Product_Category.objects.create(category_name="Groceries", description="Daily Life Product", created_at=now)
    
    def test_fetch_all_product_categories_success(self):
        """
        Test if the function fetches all product categories successfully.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNotNone(product_categories, "Product categories should not be None.")
        self.assertEqual(product_categories.count(), 3, "The function did not return all product categories.")
        self.assertEqual(message, "Fetched all product categories successfully!", "Success message is incorrect.")

    @mock.patch('products.models.Product_Category.objects.all', side_effect=DatabaseError("Database Error"))
    def test_fetch_all_product_categories_database_error(self, mock_all):
        """
        Test if the function handles DatabaseError correctly.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on DatabaseError.")
        self.assertEqual(message, "An unexpected error in Database occurred! Please try again later.", "Error message is incorrect.")

    @mock.patch('products.models.Product_Category.objects.all', side_effect=IntegrityError("Integrity Error"))
    def test_fetch_all_product_categories_integrity_error(self, mock_all):
        """
        Test if the function handles IntegrityError correctly.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on IntegrityError.")
        self.assertEqual(message, "An unexpected error in Database occurred! Please try again later.", "Error message is incorrect.")

    @mock.patch('products.models.Product_Category.objects.all', side_effect=OperationalError("Operational Error"))
    def test_fetch_all_product_categories_operational_error(self, mock_all):
        """
        Test if the function handles OperationalError correctly.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on OperationalError.")
        self.assertEqual(message, "An unexpected error in Database occurred! Please try again later.", "Error message is incorrect.")

    @mock.patch('products.models.Product_Category.objects.all', side_effect=ProgrammingError("Programming Error"))
    def test_fetch_all_product_categories_programming_error(self, mock_all):
        """
        Test if the function handles ProgrammingError correctly.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on ProgrammingError.")
        self.assertEqual(message, "An unexpected error in Database occurred! Please try again later.", "Error message is incorrect.")

class TestManageProductsSubCategories(TestCase):
    
    def setUp(self):
        # create sample data with timezone-aware datetime
        now = timezone.now()
        self.category = Product_Category.objects.create(category_name="Electronics", description="Electronic Items", created_at=now)
        sub_category1 = Product_Sub_Category.objects.create(sub_category_name="Mobile Phones", description="Smartphones", created_at=now)
        sub_category2 = Product_Sub_Category.objects.create(sub_category_name="Laptops", description="Portable Computers", created_at=now)
        sub_category1.category_id.set([self.category])
        sub_category2.category_id.set([self.category])
    
    def test_fetch_all_product_sub_categories_for_a_category_success(self):
        """
        Test if the function fetches all product sub-categories for a category successfully.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category.pk)
        self.assertIsNotNone(sub_categories, "Product sub-categories should not be None.")
        self.assertEqual(sub_categories.count(), 2, "The function did not return all product sub-categories.")
        self.assertEqual(message, "Fetched all product sub-categories for a category successfully!", "Success message is incorrect.")

    @mock.patch('products.models.Product_Sub_Category.objects.filter', side_effect=DatabaseError("Database Error"))
    def test_fetch_all_product_sub_categories_for_a_category_database_error(self, mock_filter):
        """
        Test if the function handles DatabaseError correctly.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category.pk)
        self.assertIsNone(sub_categories, "Product sub-categories should be None on DatabaseError.")
        self.assertEqual(message, "An unexpected error in Database occurred! Please try again later.", "Error message is incorrect.")

    @mock.patch('products.models.Product_Sub_Category.objects.filter', side_effect=OperationalError("Operational Error"))
    def test_fetch_all_product_sub_categories_for_a_category_operational_error(self, mock_filter):
        """
        Test if the function handles OperationalError correctly.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category.pk)
        self.assertIsNone(sub_categories, "Product sub-categories should be None on OperationalError.")
        self.assertEqual(message, "An unexpected error in server occurred! Please try again later.", "Error message is incorrect.")

    @mock.patch('products.models.Product_Sub_Category.objects.filter', side_effect=ProgrammingError("Programming Error"))
    def test_fetch_all_product_sub_categories_for_a_category_programming_error(self, mock_filter):
        """
        Test if the function handles ProgrammingError correctly.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category.pk)
        self.assertIsNone(sub_categories, "Product sub-categories should be None on ProgrammingError.")
        self.assertEqual(message, "An unexpected error in server occurred! Please try again later.", "Error message is incorrect.")

    @mock.patch('products.models.Product_Sub_Category.objects.filter', side_effect=IntegrityError("Integrity Error"))
    def test_fetch_all_product_sub_categories_for_a_category_integrity_error(self, mock_filter):
        """
        Test if the function handles IntegrityError correctly.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category.pk)
        self.assertIsNone(sub_categories, "Product sub-categories should be None on IntegrityError.")
        self.assertEqual(message, "Same type exists in Database!", "Error message is incorrect.")
    
#     def test_create_new_product_type_success(self):
#         """
#         Test creating a new product type successfully.
#         """
#         success, message = ManageProducts.create_product_type("Furnitures", "Furniture goods")
#         self.assertTrue(success, "The function should return True on successful creation.")
#         self.assertEqual(message, "New Product type Furnitures successfully added!",
#                          "The success message is incorrect.")
#         self.assertEqual(Product_type.objects.filter(type="Furnitures").count(), 1,
#                          "The new product type should be added to the database.")

#     def test_create_duplicate_product_type(self):
#         """
#         Test creating a product type that already exists.
#         """
#         success, message = ManageProducts.create_product_type("cosmEtiCs", "Duplicate electronic items")
#         self.assertFalse(success, "The function should return False for duplicate types.")
#         self.assertEqual(message, "Same type exists in Database!",
#                          "The duplicate type message is incorrect.")
#         self.assertEqual(Product_type.objects.filter(type="cosmEtiCs").count(), 0,
#                          "No duplicate entries should be created in the database.")
    
#     @mock.patch('products.models.Product_type.objects.create', side_effect=DatabaseError("Database Error"))
#     def test_create_product_type_database_error(self, mock_create):
#         """
#         Test handling of a DatabaseError during product type creation.
#         """
#         success, message = ManageProducts.create_product_type("Toys", "Toys and games")
#         self.assertFalse(success, "The function should return False on a DatabaseError.")
        
#         self.assertEqual(ErrorLogs.objects.filter(error_type="DatabaseError").count(), 1,
#                          "A DatabaseError should be logged in the ErrorLogs model.")

# class TestUpdateProductType(TestCase):
#     def setUp(self):
#         """
#         Set up initial data for testing.
#         """
#         self.product_type1 = Product_type.objects.create(type="Electronics", description="Electronic items")
#         self.product_type2 = Product_type.objects.create(type="Furniture", description="Furniture items")

#     def test_update_product_type_success(self):
#         """
#         Test successfully updating a product type.
#         """
#         success, message = ManageProducts.update_product_type(
#             product_type_pk=self.product_type1.pk, 
#             new_type="Updated Electronics", 
#             description="Updated description for electronics"
#         )
#         self.assertTrue(success, "The function should return True for a successful update.")
#         self.assertEqual(message, "Product Type updated successfully!", "The success message is incorrect.")

#         # Verify the updates
#         updated_product_type = Product_type.objects.get(pk=self.product_type1.pk)
#         self.assertEqual(updated_product_type.type, "Updated Electronics", "The product type name was not updated.")
#         self.assertEqual(updated_product_type.description, "Updated description for electronics",
#                          "The product type description was not updated.")

#     def test_update_duplicate_product_type(self):
#         """
#         Test updating a product type when a duplicate exists.
#         """
#         success, message = ManageProducts.update_product_type(
#             product_type_pk=self.product_type1.pk, 
#             new_type="Furniture",  # Duplicate type
#             description="Trying to update to a duplicate type"
#         )
#         self.assertFalse(success, "The function should return False for a duplicate type.")
#         self.assertEqual(message, "Same type exists in Database!", "The duplicate type message is incorrect.")

#     def test_update_nonexistent_product_type(self):
#         """
#         Test updating a non-existent product type.
#         """
#         success, message = ManageProducts.update_product_type(
#             product_type_pk=9999,  # Non-existent primary key
#             new_type="Nonexistent",
#             description="Trying to update a non-existent product type"
#         )
#         self.assertFalse(success, "The function should return False for a non-existent product type.")
#         self.assertEqual(message, "Product Type does not exist!", "The error message for a non-existent product type is incorrect.")

#     @mock.patch('products.models.Product_type.objects.get', side_effect=DatabaseError("Database Error"))
#     def test_update_product_type_database_error(self, mock_get):
#         """
#         Test handling of a DatabaseError during product type update.
#         """
#         success, message = ManageProducts.update_product_type(
#             product_type_pk=self.product_type1.pk, 
#             new_type="New Type",
#             description="Description"
#         )
#         self.assertFalse(success, "The function should return False on a DatabaseError.")
#         self.assertEqual(message, "An unexpected error in Database occurred while updating Product Type! Please try again later.",
#                          "The error message for DatabaseError is incorrect.")
#         self.assertEqual(ErrorLogs.objects.filter(error_type="DatabaseError").count(), 1,
#                          "A DatabaseError should be logged in the ErrorLogs model.")

#     @mock.patch('products.models.Product_type.objects.get', side_effect=OperationalError("Operational Error"))
#     def test_update_product_type_operational_error(self, mock_get):
#         """
#         Test handling of an OperationalError during product type update.
#         """
#         success, message = ManageProducts.update_product_type(
#             product_type_pk=self.product_type1.pk, 
#             new_type="New Type",
#             description="Description"
#         )
#         self.assertFalse(success, "The function should return False on an OperationalError.")
#         self.assertEqual(message, "An unexpected error in server occurred while updating Product Type! Please try again later.",
#                          "The error message for OperationalError is incorrect.")
#         self.assertEqual(ErrorLogs.objects.filter(error_type="OperationalError").count(), 1,
#                          "An OperationalError should be logged in the ErrorLogs model.")

#     @mock.patch('products.models.Product_type.objects.get', side_effect=ProgrammingError("Programming Error"))
#     def test_update_product_type_programming_error(self, mock_get):
#         """
#         Test handling of a ProgrammingError during product type update.
#         """
#         success, message = ManageProducts.update_product_type(
#             product_type_pk=self.product_type1.pk, 
#             new_type="New Type",
#             description="Description"
#         )
#         self.assertFalse(success, "The function should return False on a ProgrammingError.")
#         self.assertEqual(message, "An unexpected error in server occurred while updating Product Type! Please try again later.",
#                          "The error message for ProgrammingError is incorrect.")
#         self.assertEqual(ErrorLogs.objects.filter(error_type="ProgrammingError").count(), 1,
#                          "A ProgrammingError should be logged in the ErrorLogs model.")

#     @mock.patch('products.models.Product_type.objects.get', side_effect=IntegrityError("Integrity Error"))
#     def test_update_product_type_integrity_error(self, mock_get):
#         """
#         Test handling of an IntegrityError during product type update.
#         """
#         success, message = ManageProducts.update_product_type(
#             product_type_pk=self.product_type1.pk, 
#             new_type="New Type",
#             description="Description"
#         )
#         self.assertFalse(success, "The function should return False on an IntegrityError.")
#         self.assertEqual(message, "Same type exists in Database!", "The error message for IntegrityError is incorrect.")
#         self.assertEqual(ErrorLogs.objects.filter(error_type="IntegrityError").count(), 1,
#                          "An IntegrityError should be logged in the ErrorLogs model.")

# class TestDeleteProductType(TestCase):
#     def setUp(self):
#         """
#         Set up initial data for testing.
#         """
#         self.product_type1 = Product_type.objects.create(type="Electronics", description="Electronic items")
#         self.product_type2 = Product_type.objects.create(type="Furniture", description="Furniture items")

#     def test_delete_product_type_success(self):
#         """
#         Test successfully deleting an existing product type.
#         """
#         success, message = ManageProducts.delete_product_type(self.product_type1.pk)
#         self.assertTrue(success, "The function should return True for successful deletion.")
#         self.assertEqual(message, "Product Type deleted successfully!", "The success message is incorrect.")
#         self.assertFalse(Product_type.objects.filter(pk=self.product_type1.pk).exists(),
#                          "The product type should be deleted from the database.")

#     def test_delete_nonexistent_product_type(self):
#         """
#         Test attempting to delete a non-existent product type.
#         """
#         success, message = ManageProducts.delete_product_type(9999)  # Non-existent primary key
#         self.assertFalse(success, "The function should return False for a non-existent product type.")
#         self.assertEqual(message, "Product Type does not exist!", "The error message for a non-existent product type is incorrect.")

#     @mock.patch('products.models.Product_type.objects.get', side_effect=DatabaseError("Database Error"))
#     def test_delete_product_type_database_error(self, mock_get):
#         """
#         Test handling of a DatabaseError during deletion.
#         """
#         success, message = ManageProducts.delete_product_type(self.product_type1.pk)
#         self.assertFalse(success, "The function should return False on a DatabaseError.")
#         self.assertEqual(message, "An unexpected error in Database occurred while deleting Product Type! Please try again later.",
#                          "The error message for DatabaseError is incorrect.")
#         self.assertEqual(ErrorLogs.objects.filter(error_type="DatabaseError").count(), 1,
#                          "A DatabaseError should be logged in the ErrorLogs model.")

#     @mock.patch('products.models.Product_type.objects.get', side_effect=OperationalError("Operational Error"))
#     def test_delete_product_type_operational_error(self, mock_get):
#         """
#         Test handling of an OperationalError during deletion.
#         """
#         success, message = ManageProducts.delete_product_type(self.product_type1.pk)
#         self.assertFalse(success, "The function should return False on an OperationalError.")
#         self.assertEqual(message, "An unexpected error in server occurred while deleting Product Type! Please try again later.",
#                          "The error message for OperationalError is incorrect.")
#         self.assertEqual(ErrorLogs.objects.filter(error_type="OperationalError").count(), 1,
#                          "An OperationalError should be logged in the ErrorLogs model.")

#     @mock.patch('products.models.Product_type.objects.get', side_effect=ProgrammingError("Programming Error"))
#     def test_delete_product_type_programming_error(self, mock_get):
#         """
#         Test handling of a ProgrammingError during deletion.
#         """
#         success, message = ManageProducts.delete_product_type(self.product_type1.pk)
#         self.assertFalse(success, "The function should return False on a ProgrammingError.")
#         self.assertEqual(message, "An unexpected error in server occurred while deleting Product Type! Please try again later.",
#                          "The error message for ProgrammingError is incorrect.")
#         self.assertEqual(ErrorLogs.objects.filter(error_type="ProgrammingError").count(), 1,
#                          "A ProgrammingError should be logged in the ErrorLogs model.")

#     @mock.patch('products.models.Product_type.objects.get', side_effect=IntegrityError("Integrity Error"))
#     def test_delete_product_type_integrity_error(self, mock_get):
#         """
#         Test handling of an IntegrityError during deletion.
#         """
#         success, message = ManageProducts.delete_product_type(self.product_type1.pk)
#         self.assertFalse(success, "The function should return False on an IntegrityError.")
#         self.assertEqual(message, "Same type exists in Database!", "The error message for IntegrityError is incorrect.")
#         self.assertEqual(ErrorLogs.objects.filter(error_type="IntegrityError").count(), 1,
#                          "An IntegrityError should be logged in the ErrorLogs model.")