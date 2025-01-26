from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomerUser
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
# Create your views here.

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
                password=make_password(password),
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