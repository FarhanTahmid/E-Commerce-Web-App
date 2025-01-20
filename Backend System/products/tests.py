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

        #creating product brand
        self.brand1 = Product_Brands.objects.create(brand_name="Loreal", brand_country="USA",brand_description="Loreal Paris",
                                                    brand_established_year= 1909,is_own_brand=False,created_at=now)
        self.brand2 = Product_Brands.objects.create(brand_name="Dove", brand_country="USA",brand_description="Loreal Paris",
                                                    brand_established_year= 2000,is_own_brand=True,created_at=now)
        #creating product flavours
        self.product_flavour1 = Product_Flavours.objects.create(product_flavour_name="Vanilla", created_at=now)
        self.product_flavour2 = Product_Flavours.objects.create(product_flavour_name="Strawberry", created_at=now)

        #creating products
        self.product1 = Product.objects.create(product_name="Loreal Moisturizer", product_brand=self.brand1,
                                       product_description="A moisturizer by Loreal", product_summary="Hydrating moisturizer",
                                       product_ingredients="Water, Glycerin", product_usage_direction="Apply daily", created_at=now)
        self.product1.product_category.set([self.category_skincare])
        self.product1.product_sub_category.set([self.sub_category1,self.sub_category2])
        self.product1.product_flavours.set([self.product_flavour1])

        self.product2 = Product.objects.create(product_name="Dove Cleanser", product_brand=self.brand2,
                                            product_description="A cleanser by Dove", product_summary="Gentle cleanser",
                                            product_ingredients="Water, Sodium Laureth Sulfate", product_usage_direction="Use twice daily", created_at=now)
        self.product2.product_category.set([self.category_skincare])
        self.product2.product_sub_category.set([self.sub_category2])
        self.product2.product_flavours.set([self.product_flavour2])

        self.product3 = Product.objects.create(product_name="Loreal Shampoo", product_brand=self.brand1,
                                            product_description="A shampoo by Loreal", product_summary="Cleansing shampoo",
                                            product_ingredients="Water, Sodium Laureth Sulfate", product_usage_direction="Use as needed", created_at=now)
        self.product3.product_category.set([self.category_haircare])
        self.product3.product_sub_category.set([self.sub_category3])
        self.product3.product_flavours.set([self.product_flavour1, self.product_flavour2])

        self.product4 = Product.objects.create(product_name="Dove Perfume", product_brand=self.brand2,
                                            product_description="A perfume by Dove", product_summary="Long-lasting fragrance",
                                            product_ingredients="Alcohol, Fragrance", product_usage_direction="Spray on pulse points", created_at=now)
        self.product4.product_category.set([self.category_fragrance])
        self.product4.product_sub_category.set([self.sub_category4])
        self.product4.product_flavours.set([self.product_flavour1])

        self.product5 = Product.objects.create(product_name="Loreal Lipstick", product_brand=self.brand1,
                                            product_description="A lipstick by Loreal", product_summary="Matte lipstick",
                                            product_ingredients="Wax, Pigment", product_usage_direction="Apply on lips", created_at=now)
        self.product5.product_category.set([self.category_makeup])
        self.product5.product_sub_category.set([self.sub_category5])
        self.product5.product_flavours.set([self.product_flavour2])

        #creating product sku
        self.product_sku1 = Product_SKU.objects.create(product_id=self.product1,product_color="white",product_price=25.3,product_stock=100,created_at=now)
        self.product_sku2 = Product_SKU.objects.create(product_id=self.product1,product_color="silver",product_price=50,product_stock=50,created_at=now)

    def test_fetch_product_categories_success(self):
        """
        Test if the function fetches all product categories successfully.
        """
        product_categories, message = ManageProducts.fetch_product_categories()
        self.assertIsNotNone(product_categories, "Product categories should not be None.")
        self.assertEqual(product_categories.count(), 4, "The function did not return all product categories.")
        self.assertEqual(message, "Fetched all product categories successfully!", "Success message is incorrect.")

    def test_fetch_a_product_category(self):

        """
        Test if the function fetches all product categories successfully.
        """
        product_category, message = ManageProducts.fetch_product_categories(product_category_pk=self.category_haircare.pk)
        self.assertIsNotNone(product_category, "Product category should not be None.")
        self.assertEqual(message, "Product categories successfully!", "Success message is incorrect.")


    @mock.patch('products.models.Product_Category.objects.all', side_effect=DatabaseError("Database Error"))
    def test_fetch_all_product_categories_database_error(self, mock_all):
        """
        Test if the function handles DatabaseError correctly.
        """
        product_categories, message = ManageProducts.fetch_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on DatabaseError.")
        

    @mock.patch('products.models.Product_Category.objects.all', side_effect=IntegrityError("Integrity Error"))
    def test_fetch_all_product_categories_integrity_error(self, mock_all):
        """
        Test if the function handles IntegrityError correctly.
        """
        product_categories, message = ManageProducts.fetch_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on IntegrityError.")
    

    @mock.patch('products.models.Product_Category.objects.all', side_effect=OperationalError("Operational Error"))
    def test_fetch_all_product_categories_operational_error(self, mock_all):
        """
        Test if the function handles OperationalError correctly.
        """
        product_categories, message = ManageProducts.fetch_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on OperationalError.")
    

    @mock.patch('products.models.Product_Category.objects.all', side_effect=ProgrammingError("Programming Error"))
    def test_fetch_all_product_categories_programming_error(self, mock_all):
        """
        Test if the function handles ProgrammingError correctly.
        """
        product_categories, message = ManageProducts.fetch_product_categories()
        self.assertIsNone(product_categories, "Product categories should be None on ProgrammingError.")

    def test_create_new_product_category(self):
        """
        Test creating a new product category successfully.
        """
        success, message = ManageProducts.create_product_category("Perfume", "Perfume Items")
        self.assertTrue(success, "Product category should be created successfully.")
        self.assertEqual(message, "New Product category. Perfume successfully added!", "Success message is incorrect.")

    def test_update_product_category(self):
        """
        Test updating a product category successfully.
        """
        success, message = ManageProducts.update_product_category(self.category_fragrance.pk, "Perfumes Updated", "Perfumes Description")
        self.assertTrue(success, "Product category should be updated successfully.")
        self.assertEqual(message, "Product Category updated successfully!", "Success message is incorrect.")
    
    def test_delete_product_category(self):
        """
        Test deleting a product category successfully.
        """
        success, message = ManageProducts.delete_product_category(self.category_haircare.pk)#deleting Haricare
        self.assertTrue(success, "Product category should be deleted successfully.")
        self.assertEqual(message, "Product Category deleted successfully!", "Success message is incorrect.")
        
    #product sub category testcases
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

    
    def test_update_product_sub_category_success(self):
        """
        Test updating a product sub-category successfully.
        """
        success, message = ManageProducts.update_product_sub_category(self.sub_category1.pk,[self.category_skincare.pk,self.category_makeup.pk,self.category_fragrance.pk], "Moistorizer", "Moistorizer to make skin soft")
        self.assertTrue(success, "Product Sub Category updated successfully!")
        self.assertEqual(message, "Product Sub Category updated successfully!", "Success message is incorrect.")

    
    def test_delete_product_sub_category_success(self):
        """
        Test deleting a product sub-category successfully.
        """
        success, message = ManageProducts.delete_product_sub_category(self.sub_category1.pk)
        self.assertTrue(success,"Product Sub Category deleted successfully!")
        self.assertEqual(message,"Product Sub Category deleted successfully!", "Delete message is incorrect.")

    #testcase for product brand
    def test_create_product_brand_success(self):
        """
        Test creating a new product brand successfully.
        """
        success, message = ManageProducts.create_product_brand("Lux", 1889,True, "USA", "Lux Paris")
        self.assertTrue(success, "Product brand should be created successfully.")
        self.assertEqual(message, "New Product brand, Lux successfully added!", "Success message is incorrect.")
    
    def test_create_product_brand_duplicate(self):
        """
        Test creating a duplicate product brand.

        """
        success,message = ManageProducts.create_product_brand("Loreal", 1909,False, "USA", "Loreal Paris")
        self.assertFalse(success,"Product brand should not be created if it already exists.")
        self.assertEqual(message,"Same brand exists in Database!", "Duplicate message is incorrect.")

    def test_fetch_product_brand(self):
        """
        Test for fetching a particular product brand.
        """

        success,message = ManageProducts.fetch_product_brand(brand_name="Loreal")
        self.assertTrue(success,"Product brand should be fetched successfully.")
        self.assertEqual(message,"Product brand fetched successfully!", "Success message is incorrect.")
    
    def test_fetch_product_brand_all(self):
        """
        Test for fetching all product brand.
        """

        success,message = ManageProducts.fetch_product_brand()
        self.assertTrue(success,"All Product brand should be fetched successfully.")
        self.assertEqual(message,"All Product brands fetched successfully!", "Success message is incorrect.")
    
    def test_fetch_product_brand_not_found(self):
        """
        Test for  product brand not found.
        """
        success,message = ManageProducts.fetch_product_brand(brand_name="GorurGhash")
        self.assertFalse(success,"Product brand not found.")
        self.assertEqual(message,"An unexpected error occurred while fetching Product brand! Please try again later.", "Error message is incorrect.")


    def test_update_product_brand_success(self):
        """
        Test updating a product brand successfully.
        """
        success, message = ManageProducts.update_product_brand(self.brand1.pk, "Loreal Updated",2009,True, "India", "Loreal Paris Updated")
        self.assertTrue(success, "Product brand should be updated successfully.")
        self.assertEqual(message, "Product brand, Loreal Updated updated successfully!", "Success message is incorrect.")

    def test_delete_product_brand_success(self):
        """
        Test deleting a product brand successfully.
        """
        success, message = ManageProducts.delete_product_brand(self.brand1.pk)
        self.assertTrue(success, "Product brand should be deleted successfully.")
        self.assertEqual(message, "Product brand deleted successfully!", "Success message is incorrect.")

    #testcase for product flavour
    def test_fetch_all_product_flavour(self):
        """
        Test for fetching all product flavours.
        """
        success,message = ManageProducts.fetch_product_flavour()
        self.assertTrue(success,"All Product flavours should be fetched successfully.")
        self.assertEqual(message,"All Product flavours fetched successfully!", "Success message is incorrect.")

    def test_fetch_a_product_flavour(self):
        """
        Test for fetching a particular product flavour.
        """
        success,message = ManageProducts.fetch_product_flavour(product_flavour_name="Vanilla")
        self.assertTrue(success,"Product flavour should be fetched successfully.")
        self.assertEqual(message,"Product flavour fetched successfully!", "Success message is incorrect.")
    
    def test_fetch_a_product_flavour_not_found(self):
        """
        Test for  product flavour not found.
        """
        success,message = ManageProducts.fetch_product_flavour(product_flavour_name="GorurGhash")
        self.assertFalse(success,"Product flavour not found.")
        self.assertEqual(message,"An unexpected error occurred while fetching product flavour! Please try again later.", "Error message is incorrect.")

    def test_create_product_flavour(self):
        """
        Test creating a new product flavour successfully.
        """
        success, message = ManageProducts.create_product_flavour("Rose")
        self.assertTrue(success, "Product flavour should be created successfully.")
        self.assertEqual(message, "New Product flavour, Rose successfully added!", "Success message is incorrect.")

    def test_create_product_flavour_duplicate(self):
        """
        Test creating a duplicate product flavour.
        """
        success,message = ManageProducts.create_product_flavour("Vanilla")
        self.assertFalse(success,"Product flavour should not be created if it already exists.")
        self.assertEqual(message,"Same flavour exists in Database!", "Duplicate message is incorrect.")

    def test_update_product_flavour_success(self):
        """
        Test updating a product flavour successfully.
        """
        success, message = ManageProducts.update_product_flavour(self.product_flavour1.pk, "Vanilla changed to icecream")
        self.assertTrue(success, "Product flavour should be updated successfully.")
        self.assertEqual(message, "Product flavour updated successfully!", "Success message is incorrect.")

    def test_delete_product_flavour(self):
        """
        Test deleting a product flavour successfully.
        """
        success, message = ManageProducts.delete_product_flavour(self.product_flavour2.pk)
        self.assertTrue(success, "Product flavour should be deleted successfully.")
        self.assertEqual(message, "Product flavour deleted successfully!", "Success message is incorrect.")


    #test for products
    def test_fetch_product_using_pk(self):
        """
        Test fetching products using pk including found and not found
        """
        success, message = ManageProducts.fetch_product(product_pk=self.product1.pk)
        self.assertTrue(success,"Product should be fetched successfully.")
        self.assertEqual(message,"Products fetched successfully!", "Success message is incorrect")

        success, message = ManageProducts.fetch_product(product_pk=100)
        self.assertFalse(success,"Product should not be fetched successfully.")
        self.assertEqual(message,"An unexpected error occurred while fetching product! Please try again later.", "Error message is incorrect")
        

    def test_fetch_product_using_product_name(self):
        """
        Test fetching products using product name including found and not found
        """
        success, message = ManageProducts.fetch_product(product_name=self.product2.product_name)
        self.assertTrue(success,"Product should be fetched successfully.")
        self.assertEqual(message,"Products fetched successfully!", "Success message is incorrect")

        success, message = ManageProducts.fetch_product(product_name="sami")
        self.assertFalse(success,"Product should not be fetched successfully.")
        self.assertEqual(message,"An unexpected error occurred while fetching product! Please try again later.", "Error message is incorrect")

        

    def test_fetch_product_using_brand(self):
        """
        Test fetching products using product brand including found and not found
        """
        success, message = ManageProducts.fetch_product(product_brand_pk=self.brand1.pk)
        self.assertTrue(success,"Products should be fetched successfully.")
        self.assertEqual(message,"Products fetched successfully!", "Success message is incorrect")

        success, message = ManageProducts.fetch_product(product_brand_pk=9)
        self.assertFalse(success,"Product should not be fetched successfully.")
        self.assertEqual(message,"No products found using this brand", "Error message is incorrect")
        

    def test_fetch_product_using_product_category_list(self):
        """
        Test fetching products using product category list including found and not found
        """
        success,message = ManageProducts.fetch_product(product_category_pk_list=[self.category_skincare.pk,self.category_haircare.pk])
        self.assertTrue(success,"Products should be fetched successfully.")
        self.assertEqual(message,"Products fetched successfully!")

        #no category found case
        success, message = ManageProducts.fetch_product(product_category_pk_list=[80000])
        self.assertFalse(success,"Product should not be fetched successfully.")
        self.assertEqual(message,"An unexpected error occurred while fetching product! Please try again later.", "Error message is incorrect")

    def test_fetch_product_using_product_sub_categories(self):
        """
        Test fetching products using product sub category list including found and not found
        """
        success,message = ManageProducts.fetch_product(product_sub_category_pk_list=[self.sub_category1.pk,self.sub_category5.pk,self.sub_category2.pk])
        self.assertTrue(success,"Products should be fetched successfully.")
        self.assertEqual(message,"Products fetched successfully!")

        success, message = ManageProducts.fetch_product(product_sub_category_pk_list=[8090])
        self.assertFalse(success,"Product should not be fetched successfully.")
        self.assertEqual(message,"An unexpected error occurred while fetching product! Please try again later.", "Error message is incorrect")

    def test_create_product(self):
        """
        Test creating product, duplicate as well
        """

        success,message = ManageProducts.create_product("Dove Lipstick",[self.category_makeup.pk,self.category_skincare.pk],
                                                        [self.sub_category1.pk,self.sub_category5.pk,self.sub_category3.pk],
                                                        "Essentials","Very Essentials",[self.product_flavour1.pk],
                                                        self.brand2.pk,"soup","free to use")
        self.assertTrue(success,"Product successfully created.")
        self.assertEqual(message,"Product, Dove Lipstick created!","Success message is incorrect")


        success,message = ManageProducts.create_product("Dove Lipstick",[self.category_makeup.pk,self.category_skincare.pk],
                                                        [self.sub_category1.pk,self.sub_category5.pk,self.sub_category3.pk],
                                                        "Essentials","Very Essentials",[self.product_flavour1.pk],
                                                        self.brand2.pk,"soup","free to use")
        self.assertFalse(success,"Product should not be created")
        self.assertEqual(message, "Same product already exists!","Error message is incorrect")

    def test_update_product(self):
        """
        Test update product
        """

        success, message = ManageProducts.update_product(self.product5.pk,self.product5.product_name,[self.category_fragrance.pk,self.category_makeup.pk],
                                                         [self.sub_category1.pk],"hii","yoo",[self.product_flavour2.pk,self.product_flavour1.pk],
                                                         self.brand2.pk,"nothing","ooo")
        self.assertTrue(success,"Product should be updated!")
        self.assertEqual(message,"Product updated successfully!","Success message is incorrect")

    def test_delete_product(self):
        """
        Test delete product
        """

        success,message = ManageProducts.delete_product(self.product5.pk)
        self.assertTrue(success,"Product should be deleted successfully!")
        self.assertEqual(message,"Product deleted successfully","Success message is incorrect")

    #test product sku
    def test_fetch_product_sku(self):
        """
        Test for fetching product sky
        """
        #fetch using pk
        success, message = ManageProducts.fetch_product_sku(pk=self.product_sku2.pk)
        self.assertTrue(success,"Product sku should be fetched successfully!")
        self.assertEqual(message,"Fetched successfully","Success message is incorrect")

        #fetch using product id
        success, message = ManageProducts.fetch_product_sku(product_id=self.product1.pk)
        self.assertTrue(success,"Product sku should be fetched successfully!")
        self.assertEqual(message,"Fetched successfully","Success message is incorrect")

        #fetch using product name
        success, message = ManageProducts.fetch_product_sku(product_name=self.product1.product_name)
        self.assertTrue(success,"Product sku should be fetched successfully!")
        self.assertEqual(message,"Fetched successfully","Success message is incorrect")

        #fetch using product sku if not found
        success, message = ManageProducts.fetch_product_sku(product_sku="sAmi5")
        self.assertFalse(success,"Product sku should not be fetched successfully!")
        self.assertEqual(message,"No sku with this code!","Error is incorrect")

    def test_create_product_sku(self):
        """
        Test for creating product sku
        """
        success, message = ManageProducts.create_product_sku(product_pk=self.product2.pk,product_price=25,product_stock=100,product_size=10)
        self.assertTrue(success,"Product sku should be created successfully!")
        self.assertEqual(message,"Product sku created successfully","Success message is incorrect")

    def test_update_product_sku(self):
        """
        Test for updating product sku
        """
        success, message = ManageProducts.update_product_sku(product_sku_pk=self.product_sku1.pk,product_id=self.product1.pk,product_price=100,product_stock=50,product_color="red",product_size=80)
        self.assertTrue(success,"Product sku should be updated successfully!")
        self.assertEqual(message,"Product sku updated with new sku id","Success message is incorrect")

    def delete_product_sku(self):
        """
        Test for deleting product
        """
        success, message = ManageProducts.delete_product_sku(product_sku_pk=self.product_sku1.pk)
        self.assertTrue(success,"Product sku should be deleted successfully!")
        self.assertEqual(message,"Product sku successfully deleted!","Success message is incorrect")

        
   
        