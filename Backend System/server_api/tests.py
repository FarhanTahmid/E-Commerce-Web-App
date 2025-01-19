from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from products.models import *
from products import product_serializers

# Create your tests here.
class ProductAPITestCases(APITestCase):
    
    def setUp(self):
        self.now = timezone.now()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.product_category1 = Product_Category.objects.create(category_name="Skincare", description="Products for skincare", created_at=self.now)
        self.product_category2= Product_Category.objects.create(category_name="Makeup", description="Products for makeup", created_at=self.now)

    def test_fetch_all_product_categories(self):
        """
        Test
        for fetching product categories
        """
        response = self.client.get('/server_api/product/categories/fetch_all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data['product_category']),2)
        expected_data = Product_Category.objects.all()
        returned_data = response.data['product_category']
        expected_data_serialized = product_serializers.Product_Category_Serializer(expected_data, many=True).data
        self.assertEqual(returned_data, expected_data_serialized)

    def test_create_product_categories(self):
        """
        Test
        for creating product categories also for duplicate as well
        """
        data = {"category_name": "Test Product", "description": "Test Description"}
        response = self.client.post('/server_api/product/categories/create/', data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],"New Product category. Test Product successfully added!")

        response = self.client.post('/server_api/product/categories/create/', data,format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Same type exists in Database!","Not Equal")

    def test_update_product_categories(self):
        """
        Test
        for updating product categories
        """
        
        data = {"category_name": "Glass Skincare", "description": "Products for glass skincare"}
        response = self.client.put(f'/server_api/product/categories/update/{self.product_category1.pk}/', data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Product Category updated successfully!")

    def test_delete_product_categories(self):
        """
        Test
        for deleting product categories
        """

        response = self.client.delete(f'/server_api/product/categories/delete/{self.product_category2.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'],"Product Category deleted successfully!")
        self.assertFalse(Product_Category.objects.filter(pk=self.product_category2.pk).exists(),False)

        #deleting again
        response = self.client.delete(f'/server_api/product/categories/delete/{self.product_category2.pk}/')
        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],"Product Category does not exist!")