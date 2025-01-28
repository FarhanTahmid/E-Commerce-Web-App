from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomCustomerManager

class CustomerSignupViewTests(APITestCase):
    """
    Test cases for the CustomerSignupView API endpoint.
    """

    def setUp(self):
        """
        Set up initial data for tests.
        """
        self.signup_url = '/customer/signup/'  # Replace with your actual endpoint URL
        self.existing_email = 'existing@example.com'
        CustomCustomerManager.objects.create(
            email=self.existing_email, 
            password='existing_password'
        )

    def test_successful_signup(self):
        """
        Test a successful signup with valid email and password.
        """
        data = {
            'email': 'new_user@example.com',
            'password': 'securepassword123',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Customer created successfully')
        self.assertTrue(CustomCustomerManager.objects.filter(email='new_user@example.com').exists())

    def test_signup_with_missing_email(self):
        """
        Test signup when the email field is missing.
        """
        data = {
            'password': 'securepassword123',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email and password are required')

    def test_signup_with_missing_password(self):
        """
        Test signup when the password field is missing.
        """
        data = {
            'email': 'new_user@example.com',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email and password are required')

    def test_signup_with_duplicate_email(self):
        """
        Test signup with an email that already exists.
        """
        data = {
            'email': self.existing_email,
            'password': 'newpassword123',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email already exists')

    def test_unexpected_error_handling(self):
        """
        Test for unexpected errors during signup.
        """
        with self.assertRaises(Exception):
            response = self.client.post(self.signup_url, None)
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn('error', response.data)
