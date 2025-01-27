from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomerUser
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated

class CustomerSignupView(APIView):
    
    """
    Handles the customer signup process for the e-commerce application.

    Features:
        - Allows users to register with an email and password.
        - Validates that email and password are provided.
        - Checks for duplicate email addresses in the database.
        - Enforces rate limiting to prevent abuse.
        - Returns informative error messages for invalid input.

    Permissions:
        - Open to all users (AllowAny).

    Rate Limiting:
        - Maximum of 5 requests per minute per IP address.

    Responses:
        - 201 Created: Customer created successfully.
        - 400 Bad Request: Missing fields, duplicate email, or invalid input.
        - 429 Too Many Requests: Rate limit exceeded.
        - 500 Internal Server Error: Unexpected server error.

    Example Request:
        POST /signup/
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }

    Example Response (Success):
        {
            "message": "Customer created successfully"
        }

    Example Response (Error - Duplicate Email):
        {
            "error": "Email already exists"
        }
    """

    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        """
        Handles the creation of a new customer account.

        Parameters:
            request (Request): The HTTP request object containing user input data.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        data = request.data
        
        try:
            email = data.get('email')
            password = data.get('password')

            # Validate required fields
            if not email or not password:
                return Response(
                    {'error': 'Email and password are required'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check for existing email
            if CustomerUser.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Email already exists'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create new customer user
            new_customer_user = CustomerUser.objects.create(
                email=email,
                password=password,
            )
            new_customer_user.save()

            return Response(
                {'message': 'Customer created successfully'},
                status=status.HTTP_201_CREATED,
            )
        except KeyError as e:
            return Response(
                {'error': f'Missing required field: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError as e:
            return Response(
                {'error': f'Invalid value: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class CustomerLoginView(APIView):
    """
    Handles the customer login process for the e-commerce application.

    Features:
        - Authenticates a user based on their email and password.
        - Issues access and refresh tokens upon successful login.
        - Implements rate limiting to prevent abuse.

    Permissions:
        - Open to all users (AllowAny).

    Rate Limiting:
        - Maximum of 5 requests per minute per IP address.

    Responses:
        - 200 OK: Login successful; returns access and refresh tokens.
        - 400 Bad Request: Missing fields, invalid credentials, or invalid data.
        - 429 Too Many Requests: Rate limit exceeded.
        - 500 Internal Server Error: Unexpected server error.

    Example Request:
        POST /login/
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }

    Example Response (Success):
        {
            "refresh": "<refresh_token>",
            "access": "<access_token>",
            "message": "Login successful"
        }

    Example Response (Error - Invalid Credentials):
        {
            "error": "Invalid email or password"
        }
    """
    
    permission_classes = [AllowAny]
    
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        data=request.data
        try:
            # Check for required fields
            email = data.get('email')
            password = data.get('password')
            if not email or not password:
                return Response(
                    {'error': 'Email and password are required'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            customer_user=authenticate(email=email,password=password)
            if customer_user is not None:
                refresh=RefreshToken.for_user(customer_user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'Login successful'
                    }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Invalid email or password'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except KeyError as e:
            return Response(
                {'error': f'Missing required field: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError as e:
            return Response(
                {'error': f'Invalid value: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class CheckCustomerIsAuthenticatedView(APIView):
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate='15/m', method='GET', block=True))
    def get(self,request):
        try:
            user=request.user
            if user.is_authenticated:
                refresh=RefreshToken.for_user(user)
                return Response({'message':'User is authenticated',
                                 'refresh':str(refresh),
                                 'access':str(refresh.access_token)
                                 },status=status.HTTP_200_OK)
            else:
                return Response({'message':'User is not authenticated'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class CustomerLogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
