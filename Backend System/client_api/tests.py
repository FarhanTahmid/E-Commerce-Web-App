from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_api_key.models import APIKey
from products.models import Product_Category  # Assuming the model is named Product_Category

class ProductCategoryListTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an API key for testing
        api_key, cls.key = APIKey.objects.create_key(name="TestKey")
        cls.headers = {"Authorization": f"Api-Key {cls.key}"}
        
        # Create sample product categories
        Product_Category.objects.create(category_name="Electronics", description="Electronic items.")
        Product_Category.objects.create(category_name="Clothing", description="Apparel and fashion.")

    def test_fetch_all_categories_success(self):
        """
        Test case for successfully fetching all product categories.
        """
        response = self.client.get("/client_api/product-categories/",headers=self.headers)
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
        
        response = self.client.get("/client_api/product-categories/", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "Fetched all product categories successfully!")

    def test_rate_limit_exceeded(self):
        """
        Test case for exceeding the rate limit.
        """
        for _ in range(20):  # Allowable limit
            response = self.client.get("/client_api/product-categories/", headers=self.headers)
            # print(f"Request {_+1}: Status Code: {response.status_code}")
        
        # Exceeding the rate limit
        response = self.client.get("/client_api/product-categories/", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

