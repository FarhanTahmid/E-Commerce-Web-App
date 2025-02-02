from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_api_key.models import APIKey
from products.models import Product_Category  # Assuming the model is named Product_Category

class ProductCategoryListTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an API key for testing
        api_key, cls.key = APIKey.objects.create_key(name="TestKey")
        cls.headers = {"HTTP_X_API_KEY": cls.key}
        
        # Create sample product categories
        Product_Category.objects.create(category_name="Electronics", description="Electronic items.")
        Product_Category.objects.create(category_name="Clothing", description="Apparel and fashion.")

    def test_fetch_all_categories_success(self):
        """
        Test case for successfully fetching all product categories.
        """
        response = self.client.get("http://localhost:8000/client_api/product-categories/", **self.headers)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["success"], True)
        # self.assertEqual(len(response.data["data"]), 2)
        # self.assertEqual(response.data["data"][0]["name"], "Electronics")
        # self.assertEqual(response.data["data"][1]["name"], "Clothing")

    # def test_fetch_no_categories(self):
    #     """
    #     Test case for when no product categories exist in the database.
    #     """
    #     # Clear all categories
    #     Product_Category.objects.all().delete()
        
    #     response = self.client.get("/client_api/product-categories/", **self.headers)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data["success"], False)
    #     self.assertEqual(response.data["message"], "No product categories found.")

    # def test_rate_limit_exceeded(self):
    #     """
    #     Test case for exceeding the rate limit.
    #     """
    #     for _ in range(10):  # Allowable limit
    #         self.client.get("/client_api/product-categories/", **self.headers)
        
    #     # Exceeding the rate limit
    #     response = self.client.get("/api/product-categories/", **self.headers)
    #     self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    # def test_missing_api_key(self):
    #     """
    #     Test case for when the API key is not provided in the request.
    #     """
    #     response = self.client.get("/client_api/product-categories/")
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    # def test_invalid_api_key(self):
    #     """
    #     Test case for when an invalid API key is provided.
    #     """
    #     headers = {"HTTP_X_API_KEY": "invalid_key"}
    #     response = self.client.get("/client_api/product-categories/", **headers)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(response.data["detail"], "Invalid API key.")

    # def test_unexpected_error(self):
    #     """
    #     Test case for handling unexpected errors.
    #     """
    #     # Mock the function to raise an exception
    #     from unittest.mock import patch

    #     with patch("products.product_management.ManageProducts.fetch_all_product_categories", side_effect=Exception("Unexpected error")):
    #         response = self.client.get("/client_api/product-categories/", **self.headers)
    #         self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    #         self.assertEqual(response.data["success"], False)
    #         self.assertEqual(response.data["message"], "An unexpected error occurred! Please try again later.")
