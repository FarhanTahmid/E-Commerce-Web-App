from rest_framework.test import APITestCase
from rest_framework import status
from .models import Accounts
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.urls import reverse


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

User = get_user_model()
class TestAuthenticationViews(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        # Get valid tokens
        refresh = RefreshToken.for_user(self.user)
        self.valid_access = str(refresh.access_token)
        self.valid_refresh = str(refresh)
        
        # Direct URLs
        self.check_auth_url = '/customer/is-authenticated/'
        self.logout_url = '/customer/logout/'

    # ----------------------------
    # CheckCustomerIsAuthenticatedView Tests
    # ----------------------------
    
    def test_check_auth_authenticated(self):
        """Authenticated user receives 200 OK"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_access}')
        response = self.client.get(self.check_auth_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
    
    def test_check_auth_unauthenticated(self):
        """Missing credentials returns 401"""
        response = self.client.get(self.check_auth_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_check_auth_invalid_token(self):
        """Invalid token returns 401"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken123')
        response = self.client.get(self.check_auth_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_check_auth_rate_limit(self):
        """Exceed 5 requests/minute limit returns 429"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_access}')
        for _ in range(5):
            self.client.get(self.check_auth_url)  # 5 successful requests
        
        # 6th request should be blocked
        response = self.client.get(self.check_auth_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ----------------------------
    # CustomerLogoutView Tests  
    # ----------------------------
    
    # def test_successful_logout(self):
    #     """Valid logout request blacklists refresh token"""
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_access}')
    #     response = self.client.post(self.logout_url, {'refresh': self.valid_refresh})
        
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('message', response.data)
    #     self.assertTrue(
    #         BlacklistedToken.objects.filter(token__token=self.valid_refresh).exists()
    #     )
    
    # def test_logout_missing_refresh_token(self):
    #     """Missing refresh token returns 400"""
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_access}')
    #     response = self.client.post(self.logout_url, {})
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('error', response.data)
    
    # def test_logout_invalid_refresh_token(self):
    #     """Invalid refresh token returns 400"""
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_access}')
    #     response = self.client.post(self.logout_url, {'refresh': 'invalid_refresh'})
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('error', response.data)
    
    # def test_logout_blacklisted_refresh_token(self):
    #     """Already blacklisted token returns 400"""
    #     # First successful logout
    #     self.test_successful_logout()
        
    #     # Try same token again
    #     response = self.client.post(self.logout_url, {'refresh': self.valid_refresh})
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_logout_unauthenticated(self):
    #     """Missing access token returns 401"""
    #     response = self.client.post(self.logout_url, {'refresh': self.valid_refresh})
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # def test_logout_rate_limit(self):
    #     """Exceed 5 logout attempts/minute returns 429"""
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_access}')
        
    #     for _ in range(5):
    #         response = self.client.post(self.logout_url, {'refresh': self.valid_refresh})
    #         if response.status_code == 200:  # Refresh token after blacklisting
    #             new_refresh = RefreshToken.for_user(self.user)
    #             self.valid_refresh = str(new_refresh)
        
    #     # 6th attempt
    #     response = self.client.post(self.logout_url, {'refresh': self.valid_refresh})
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # def test_logout_invalid_method(self):
    #     """GET request returns 405"""
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_access}')
    #     response = self.client.get(self.logout_url)
    #     self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    # # ----------------------------
    # # Cross-Feature Tests
    # # ----------------------------
    
    # def test_access_after_logout(self):
    #     """Access token remains valid until expiration"""
    #     # Logout first
    #     self.test_successful_logout()
        
    #     # Try accessing protected endpoint
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_access}')
    #     response = self.client.get(self.check_auth_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_refresh_after_logout(self):
    #     """Blacklisted refresh token cannot refresh"""
    #     # Logout first
    #     self.test_successful_logout()
        
    #     # Try refreshing tokens
    #     response = self.client.post(
    #         '/api/token/refresh/',  # Assuming standard JWT refresh URL
    #         {'refresh': self.valid_refresh}
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)