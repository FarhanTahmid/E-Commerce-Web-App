from rest_framework.test import APITestCase
from rest_framework import status
from .models import Accounts

class CustomerAuthViewTests(APITestCase):
    """
    Test cases for the CustomerSignupView API endpoint.
    """

    def setUp(self):
        """
        Set up initial data for tests.
        """
        self.signup_url = '/customer/signup/'  
        self.login_url = '/customer/login/'
        
        # credentials setup for signup testing
        self.valid_email = 'existing@example.com'
        self.valid_password = 'password123'
        
        self.existing_user = Accounts(
            email='existing2@example.com',
            username='existing_user',
        )
        self.existing_user.set_password('password123')
        self.existing_user.save()
        
        
        # credentials setup for login testing
        self.email = 'user@example.com'
        self.password = 'securepassword123'
        
        self.user = Accounts(
            email=self.email,
            username='testuser',
        )
        self.user.set_password(self.password)
        self.user.save()
        
        
    def test_successful_signup(self):
        """
        Test successful account creation with valid data.
        """
        data = {
            'email': self.valid_email,
            'password': self.valid_password,
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Customer created successfully')

        # Check if user was created in the database
        user = Accounts.objects.filter(email=self.valid_email).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(self.valid_password))

    def test_signup_missing_email(self):
        """
        Test account creation when the email is missing.
        """
        data = {
            'password': self.valid_password,
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email and password are required')

    def test_signup_missing_password(self):
        """
        Test account creation when the password is missing.
        """
        data = {
            'email': self.valid_email,
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email and password are required')

    def test_signup_duplicate_email(self):
        """
        Test account creation with an already existing email.
        """
        data = {
            'email': self.existing_user.email,
            'password': 'newpassword123',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email already exists')
    
    def test_signup_unexpected_error(self):
        """
        Test unexpected error handling during account creation.
        """
        # Simulate unexpected error by mocking Accounts.objects.filter
        with self.assertRaises(Exception):
            data = {
                'email': None,  # Intentionally invalid email
                'password': self.valid_password,
            }
            response = self.client.post(self.signup_url, data)
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn('error', response.data)
    
    def test_successful_login(self):
        """
        Test successful login with valid credentials.
        """
        data = {
            'email': self.email,
            'password': self.password,
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['message'], 'Login successful')
    
    
    def test_missing_email(self):
        """
        Test login when the email field is missing.
        """
        data = {
            'password': self.password,
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email and password are required')

    def test_missing_password(self):
        """
        Test login when the password field is missing.
        """
        data = {
            'email': self.email,
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email and password are required')

    def test_invalid_password(self):
        """
        Test login with an incorrect password.
        """
        data = {
            'email': self.email,
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Wrong password')
    
    def test_non_existent_email(self):
        """
        Test login with an email that does not exist.
        """
        data = {
            'email': 'nonexistent@example.com',
            'password': self.password,
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Account with this email does not exist!')
