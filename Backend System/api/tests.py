from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from products import product_management
from django.utils import timezone

# Create your tests here.
class ProductAPITestCases(APITestCase):
    
    def setUp(self):
        self.now = timezone.now()

    def test_create_product(self):
        """
        Test
        for creating product also for duplicate as well
        """
        data = {"category_name": "Test Product", "description": "Test Description"}
        response = self.client.post('/api/product/create/', data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"New Product category. Test Product successfully added!")

        response = self.client.post('/api/product/create/', data,format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Same type exists in Database!","Not Equal")

