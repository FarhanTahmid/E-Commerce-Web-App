from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from system.models import Accounts
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from json.decoder import JSONDecodeError
# Create your views here.

class CustomerSignupView(APIView):
    """
    Handles customer signup for the e-commerce application.

    This API endpoint allows users to create an account by providing their email and password. 
    It validates the input, checks for duplicate emails, and hashes the password using Django's 
    default password hashing system before saving the user.

    Features:
        - Creates a new customer account with a unique email and username.
        - Validates input fields and ensures no duplicate accounts are created.
        - Implements rate limiting to prevent abuse.
        - Returns informative responses for success or failure.

    Permissions:
        - Open to all users (AllowAny).

    Rate Limiting:
        - Maximum of 5 requests per minute per IP address.

    Responses:
        - 201 Created: User created successfully.
        - 400 Bad Request: Missing fields, invalid data, or duplicate email.
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

    Input Data (JSON):
        - email (str): The unique email address for the customer. Required.
        - password (str): The password for the account. Required.

    Workflow:
        1. Extracts the `email` and `password` fields from the request data.
        2. Validates that both fields are provided.
        3. Checks if an account with the given email already exists.
        4. Extracts the username from the email (everything before the `@` symbol).
        5. Creates a new `Accounts` user instance, hashes the password using `set_password()`, and saves the user.
        6. Returns a success response upon successful account creation.

    Error Handling:
        - Returns a `400 Bad Request` if required fields are missing or invalid.
        - Returns a `400 Bad Request` if the email already exists in the database.
        - Returns a `500 Internal Server Error` for unexpected errors.

    Returns:
        Response: A JSON response indicating success or failure.

    Example Usage:
        Request:
            POST /signup/
            {
                "email": "user@example.com",
                "password": "securepassword123"
            }

        Success Response:
            {
                "message": "Customer created successfully"
            }

        Error Response (Missing Fields):
            {
                "error": "Email and password are required"
            }

        Error Response (Duplicate Email):
            {
                "error": "Email already exists"
            }
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
            if Accounts.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Email already exists'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create new customer user
            new_customer_user = Accounts(
                email=email,
                username=email.split('@')[0],
            )
            new_customer_user.set_password(password)
            new_customer_user.save()

            return Response(
                {'message': 'Customer created successfully'},
                status=status.HTTP_201_CREATED,
            )
        except JSONDecodeError as e:
            return Response(
                {'error': 'Invalid JSON format'},
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

class CustomerLoginView(APIView):
    def post(self, request):
        pass