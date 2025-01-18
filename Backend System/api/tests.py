from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your tests here.
class ProductAPITestCases(APITestCase):
    
    def setUp(self):
        self.now = timezone.now()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

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

