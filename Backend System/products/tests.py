from django.test import TestCase
from django.utils import timezone
from products.models import *
from products.product_management import ManageProducts
from unittest import mock
from django.db import *
from system.models import *
# Create your tests here.

class TestManageProducts(TestCase):
    
    def setUp(self):
        # create sample data with timezone-aware datetime
        now = timezone.now()
        # Create categories
        self.category_skincare = Product_Category.objects.create(category_name="Skincare", description="Products for skincare", created_at=now)
        self.category_makeup = Product_Category.objects.create(category_name="Makeup", description="Products for makeup", created_at=now)
        self.category_haircare = Product_Category.objects.create(category_name="Haircare", description="Products for haircare", created_at=now)
        self.category_fragrance = Product_Category.objects.create(category_name="Fragrance", description="Products for fragrance", created_at=now)
        
        # Create sub-categories
        self.sub_category1 = Product_Sub_Category.objects.create(sub_category_name="Moisturizers", description="Products to moisturize skin", created_at=now)
        self.sub_category2 = Product_Sub_Category.objects.create(sub_category_name="Cleansers", description="Products to cleanse skin", created_at=now)
        self.sub_category3 = Product_Sub_Category.objects.create(sub_category_name="Shampoos", description="Products to clean hair", created_at=now)
        self.sub_category4 = Product_Sub_Category.objects.create(sub_category_name="Perfumes", description="Fragrance products", created_at=now)
        self.sub_category5 = Product_Sub_Category.objects.create(sub_category_name="Lipsticks", description="Lip makeup products", created_at=now)
        
        # Assign sub-categories to categories
        self.sub_category1.category_id.set([self.category_skincare])
        self.sub_category2.category_id.set([self.category_skincare])
        self.sub_category3.category_id.set([self.category_haircare])
        self.sub_category4.category_id.set([self.category_fragrance])
        self.sub_category5.category_id.set([self.category_makeup])
    
    def test_fetch_all_product_categories_success(self):
        """
        Test if the function fetches all product categories successfully.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNotNone(product_categories, "Product categories should not be None.")
        self.assertEqual(product_categories.count(), 4, "The function did not return all product categories.")
        self.assertEqual(message, "Fetched all product categories successfully!", "Success message is incorrect.")

    @mock.patch('products.models.Product_Category.objects.all', side_effect=DatabaseError("Database Error"))
    def test_fetch_all_product_categories_database_error(self, mock_all):
        """
        Test if the function handles DatabaseError correctly.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on DatabaseError.")
        

    @mock.patch('products.models.Product_Category.objects.all', side_effect=IntegrityError("Integrity Error"))
    def test_fetch_all_product_categories_integrity_error(self, mock_all):
        """
        Test if the function handles IntegrityError correctly.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on IntegrityError.")
    

    @mock.patch('products.models.Product_Category.objects.all', side_effect=OperationalError("Operational Error"))
    def test_fetch_all_product_categories_operational_error(self, mock_all):
        """
        Test if the function handles OperationalError correctly.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on OperationalError.")
    

    @mock.patch('products.models.Product_Category.objects.all', side_effect=ProgrammingError("Programming Error"))
    def test_fetch_all_product_categories_programming_error(self, mock_all):
        """
        Test if the function handles ProgrammingError correctly.
        """
        product_categories, message = ManageProducts.fetch_all_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on ProgrammingError.")

    def create_new_product_category(self):
        """
        Test creating a new product category successfully.
        """
        success, message = ManageProducts.create_product_category("Perfume", "Perfume Items")
        self.assertTrue(success, "Product category should be created successfully.")
        self.assertEqual(message, "New Product category, Electronics successfully added!", "Success message is incorrect.")

    def update_product_category(self):
        """
        Test updating a product category successfully.
        """
        success, message = ManageProducts.update_product_category(5, "Perfumes Updated", "Perfumes Description")
        self.assertTrue(success, "Product category should be updated successfully.")
        self.assertEqual(message, "Product Category updated successfully!", "Success message is incorrect.")
    
    def delete_product_category(self):
        """
        Test deleting a product category successfully.
        """
        success, message = ManageProducts.delete_product_category(3)#deleting Haricare
        self.assertTrue(success, "Product category should be deleted successfully.")
        self.assertEqual(message, "Product Category deleted successfully!", "Success message is incorrect.")
        
    
    def test_fetch_all_product_sub_categories_for_a_category_success(self):
        """
        Test if the function fetches all product sub-categories for a category successfully.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category_skincare.pk)
        self.assertIsNotNone(sub_categories, "Product sub-categories should not be None.")
        self.assertEqual(sub_categories.count(), 2, "The function did not return all product sub-categories.")
        self.assertEqual(message, "Fetched all product sub-categories for a category successfully!", "Success message is incorrect.")

    @mock.patch('products.models.Product_Sub_Category.objects.filter', side_effect=DatabaseError("Database Error"))
    def test_fetch_all_product_sub_categories_for_a_category_database_error(self, mock_filter):
        """
        Test if the function handles DatabaseError correctly.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category_skincare.pk)
        self.assertIsNone(sub_categories, "Product sub-categories should be None on DatabaseError.")
        
    @mock.patch('products.models.Product_Sub_Category.objects.filter', side_effect=OperationalError("Operational Error"))
    def test_fetch_all_product_sub_categories_for_a_category_operational_error(self, mock_filter):
        """
        Test if the function handles OperationalError correctly.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category_skincare.pk)
        self.assertIsNone(sub_categories, "Product sub-categories should be None on OperationalError.")
        
    @mock.patch('products.models.Product_Sub_Category.objects.filter', side_effect=ProgrammingError("Programming Error"))
    def test_fetch_all_product_sub_categories_for_a_category_programming_error(self, mock_filter):
        """
        Test if the function handles ProgrammingError correctly.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category_skincare.pk)
        self.assertIsNone(sub_categories, "Product sub-categories should be None on ProgrammingError.")
       
    @mock.patch('products.models.Product_Sub_Category.objects.filter', side_effect=IntegrityError("Integrity Error"))
    def test_fetch_all_product_sub_categories_for_a_category_integrity_error(self, mock_filter):
        """
        Test if the function handles IntegrityError correctly.
        """
        sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(self.category_skincare.pk)
        self.assertIsNone(sub_categories, "Product sub-categories should be None on IntegrityError.")
        
    
    #testcases for create product sub category
    def test_create_product_sub_category_success(self):
        """
        Test creating a new product sub-category successfully.
        """
        success, message = ManageProducts.create_product_sub_category(self.category_makeup.pk, "Hair Spray", "HairSpray Item")
        self.assertTrue(success, "Product sub-category should be created successfully.")
        self.assertEqual(message, "New Product sub-category, Hair Spray successfully added!", "Success message is incorrect.")
    
    def test_create_product_sub_category_duplicate(self):
        """
        Test creating a duplicate product sub-category.
        """
        success, message = ManageProducts.create_product_sub_category(self.category_skincare.pk, "Moisturizers", "Moisturizers Item")
        self.assertFalse(success, "Product sub-category should not be created if it already exists.")
        self.assertEqual(message, "Same type exists in Database!", "Duplicate message is incorrect.")

    #testcase for update product sub category
    def test_update_product_sub_category_success(self):
        """
        Test updating a product sub-category successfully.
        """
        success, message = ManageProducts.update_product_sub_category(self.sub_category1.pk,[self.category_skincare.pk,self.category_makeup.pk], "Moistorizer", "Moistorizer to make skin soft")
        self.assertTrue(success, "Product Sub Category updated successfully!")
        self.assertEqual(message, "Product Sub Category updated successfully!", "Success message is incorrect.")


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