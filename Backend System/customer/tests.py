from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomerUser
from django.contrib.auth.hashers import make_password
class CustomerSignupViewTests(APITestCase):
    """
    Test cases for the CustomerSignupView API endpoint.
    """

    def setUp(self):
        """
        Set up initial data for tests.
        """
        self.signup_url = '/customer/signup/'  # Replace with your actual endpoint URL
        self.login_url='customer/login/'
        
        self.existing_email = 'existing@example.com'
        CustomerUser.objects.create(
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
        self.assertTrue(CustomerUser.objects.filter(email='new_user@example.com').exists())

    # def test_signup_with_missing_email(self):
    #     """
    #     Test signup when the email field is missing.
    #     """
    #     data = {
    #         'password': 'securepassword123',
    #     }
    #     response = self.client.post(self.signup_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('error', response.data)
    #     self.assertEqual(response.data['error'], 'Email and password are required')

    # def test_signup_with_missing_password(self):
    #     """
    #     Test signup when the password field is missing.
    #     """
    #     data = {
    #         'email': 'new_user@example.com',
    #     }
    #     response = self.client.post(self.signup_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('error', response.data)
    #     self.assertEqual(response.data['error'], 'Email and password are required')

    # def test_signup_with_duplicate_email(self):
    #     """
    #     Test signup with an email that already exists.
    #     """
    #     data = {
    #         'email': self.existing_email,
    #         'password': 'newpassword123',
    #     }
    #     response = self.client.post(self.signup_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('error', response.data)
    #     self.assertEqual(response.data['error'], 'Email already exists')

    # def test_unexpected_error_handling(self):
    #     """
    #     Test for unexpected errors during signup.
    #     """
    #     with self.assertRaises(Exception):
    #         response = self.client.post(self.signup_url, None)
    #         self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    #         self.assertIn('error', response.data)
    
    # def test_successful_login(self):
    #     """
    #     Test a successful login with valid credentials.
    #     """
    #     password=make_password('securepassword123')
    #     data = {
    #         'email': 'new_user@example.com',
    #         'password': password,
    #     }
    #     response = self.client.post(self.login_url, data)
    #     # self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertIn('refresh', response.data)
    #     # self.assertIn('access', response.data)
    #     self.assertEqual(response.data['message'], 'Login successful')


# class CustomerLoginViewTests(APITestCase):
#     """
#     Test cases for the CustomerLoginView API endpoint.
#     """

#     def setUp(self):
#         """
#         Set up initial data for tests.
#         """
#         self.login_url = '/customer/login/'  # Replace with your actual login endpoint URL
#         self.email = 'logintestuser@example.com'
#         self.password = 'securepassword123'

#         # Create a test user
#         self.user = CustomerUser.objects.create(
#             email=self.email,
#             password=makePas(self.password)
#         )

#     def test_successful_login(self):
#         """
#         Test a successful login with valid credentials.
#         """
#         data = {
#             'email': self.email,
#             'password': self.password,
#         }
#         response = self.client.post(self.login_url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('refresh', response.data)
#         self.assertIn('access', response.data)
#         self.assertEqual(response.data['message'], 'Login successful')

#     # def test_login_with_missing_email(self):
#     #     """
#     #     Test login when the email field is missing.
#     #     """
#     #     data = {
#     #         'password': self.password,
#     #     }
#     #     response = self.client.post(self.login_url, data)
#     #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#     #     self.assertIn('error', response.data)
#     #     self.assertEqual(response.data['error'], 'Email and password are required')

#     # def test_login_with_missing_password(self):
#     #     """
#     #     Test login when the password field is missing.
#     #     """
#     #     data = {
#     #         'email': self.email,
#     #     }
#     #     response = self.client.post(self.login_url, data)
#     #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#     #     self.assertIn('error', response.data)
#     #     self.assertEqual(response.data['error'], 'Email and password are required')

#     # def test_login_with_invalid_credentials(self):
#     #     """
#     #     Test login with incorrect email or password.
#     #     """
#     #     data = {
#     #         'email': self.email,
#     #         'password': 'wrongpassword',
#     #     }
#     #     response = self.client.post(self.login_url, data)
#     #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#     #     self.assertIn('error', response.data)
#     #     self.assertEqual(response.data['error'], 'Invalid email or password')

#     # def test_login_with_rate_limiting(self):
#     #     """
#     #     Test that rate limiting is enforced after 5 requests per minute.
#     #     """
#     #     data = {
#     #         'email': self.email,
#     #         'password': self.password,
#     #     }

#     #     # Make 5 valid requests
#     #     for _ in range(5):
#     #         response = self.client.post(self.login_url, data)
#     #         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     #     # Make the 6th request
#     #     response = self.client.post(self.login_url, data)
#     #     self.assertEqual(response.status_code, 429)  # HTTP 429 Too Many Requests
#     #     self.assertIn('detail', response.data)
#     #     self.assertEqual(response.data['detail'], "Request was throttled. Expected available in X seconds.")

#     # def test_unexpected_error_handling(self):
#     #     """
#     #     Test unexpected error handling in the login view.
#     #     """
#     #     # Simulate a KeyError by sending invalid JSON
#     #     response = self.client.post(self.login_url, None, content_type='application/json')
#     #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#     #     self.assertIn('error', response.data)
#     #     self.assertTrue(response.data['error'].startswith('Missing required field:'))

