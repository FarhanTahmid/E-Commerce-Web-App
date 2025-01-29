from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from system.models import Accounts
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django_ratelimit.exceptions import Ratelimited
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from json.decoder import JSONDecodeError
from datetime import timedelta

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
    
    """
    Handles customer login functionality for the e-commerce application.

    Features:
        - Authenticates a customer based on their email and password.
        - Provides access and refresh tokens upon successful login.
        - Implements rate limiting to prevent brute force attacks.

    Permissions:
        - Open to all users (AllowAny).

    Rate Limiting:
        - Limits requests to a maximum of 5 login attempts per minute per IP address.

    Responses:
        - **200 OK**: Login successful; returns access and refresh tokens.
        - **400 Bad Request**: Missing fields, invalid credentials, or incorrect data.
        - **429 Too Many Requests**: Exceeded rate limit.
        - **500 Internal Server Error**: Unexpected server error.

    Example Request:
        POST /login/
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }

    Example Responses:

        Success Response:
        {
            "refresh": "<refresh_token>",
            "access": "<access_token>",
            "message": "Login successful"
        }

        Error Response (Missing Fields):
        {
            "error": "Email and password are required"
        }

        Error Response (Invalid Password):
        {
            "error": "Wrong password"
        }

        Error Response (Non-existent Account):
        {
            "error": "Account with this email does not exist!"
        }

        Error Response (Rate Limit Exceeded):
        {
            "detail": "Request was throttled. Expected available in X seconds."
        }
    """
    
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        
        """
    Handles the login process by authenticating user credentials.

    Parameters:
        request (Request): The HTTP request object containing login data.

    Input Data (JSON):
        - email (str): The customer's email address (required).
        - password (str): The customer's password (required).

    Workflow:
        1. Extracts the `email` and `password` fields from the request data.
        2. Validates that both fields are provided.
        3. Attempts to authenticate the user using Django's `authenticate` method.
        4. If authentication succeeds:
            - Generates access and refresh tokens using `RefreshToken.for_user`.
            - Returns a success response with tokens and a message.
        5. If authentication fails:
            - Checks if the email exists in the database.
            - Returns an appropriate error message indicating whether the issue is with the password or the email.
        6. Catches and handles any unexpected errors.

    Error Handling:
        - Returns a `400 Bad Request` for missing fields or invalid credentials.
        - Returns a `400 Bad Request` if the email exists but the password is incorrect.
        - Returns a `400 Bad Request` if the email does not exist in the database.
        - Returns a `500 Internal Server Error` for unexpected errors.

    """
        
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
                # Check which input was wrong
                if Accounts.objects.filter(email=email).exists():
                    return Response(
                        {'error': 'Wrong password'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        {'error': 'Account with this email does not exist!'},
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
    """
    API endpoint to verify customer authentication status.

    This protected endpoint requires valid JWT authentication and:
    - Confirms valid authentication status for authenticated users
    - Enforces rate limiting (5 requests/minute per IP)
    - Handles various error scenarios with appropriate status codes

    Authentication:
    Requires valid JWT token in the Authorization header:
    `Authorization: Bearer <access_token>`

    Permissions:
    - User must be authenticated
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='GET', block=True))
    def get(self, request):
        """
        Handle GET request to check authentication status.

        Request Requirements:
        - Valid JWT access token in Authorization header
        - GET method only

        Responses:
        - 200 OK: User is authenticated
        - 401 UNAUTHORIZED: Missing/invalid credentials (handled automatically)
        - 429 TOO_MANY_REQUESTS: Rate limit exceeded
        - 500 INTERNAL_SERVER_ERROR: Server-side error

        Example Request:
        ```
        GET /api/check-auth/
        Headers:
            Authorization: Bearer <access_token>
        ```

        Example Success Response:
        {
            "message": "User is authenticated"
        }

        Example Error Response (429):
        {
            "error": "Request limit exceeded"
        }
        """
        try:
            # Explicit user check (redundant but demonstrates usage)
            # Permission classes already ensure authentication
            if not request.user.is_authenticated:
                raise PermissionDenied()

            return Response(
                {'message': 'User is authenticated'},
                status=status.HTTP_200_OK
            )

        except Ratelimited:
            return Response(
                {'error': 'Request limit exceeded - try again in 1 minute'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        except PermissionDenied as exc:
            return Response(
                {'error': 'Authentication credentials invalid or expired'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as exc:
            # Log full error details here (server-side)
            return Response(
                {
                    'error': 'Internal server error',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class CustomerLogoutView(APIView):
    """
    API endpoint for secure user logout functionality.

    Features:
    - Invalidates refresh token server-side (blacklists)
    - Rate limiting (5 requests/minute per IP)
    - Comprehensive error handling
    - JWT authentication requirement

    Frontend Requirements:
    1. Remove both access and refresh tokens from client storage
    2. Clear Authorization header after logout
    3. Handle 401 errors by redirecting to login

    Authentication:
    Requires valid JWT access token in Authorization header:
    `Authorization: Bearer <access_token>`
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        """
        Handle user logout by invalidating refresh token.

        Request Format:
        POST /api/auth/logout/
        Headers:
            Authorization: Bearer <access_token>
        Body (JSON):
            {
                "refresh": "<refresh_token>"
            }

        Responses:
        - 200 OK: Logout successful
        - 400 BAD_REQUEST: Missing/invalid refresh token
        - 401 UNAUTHORIZED: Invalid authentication credentials
        - 429 TOO_MANY_REQUESTS: Rate limit exceeded
        - 500 INTERNAL_SERVER_ERROR: Server error

        Frontend Directions:
        1. On successful logout (200):
           - Remove both tokens from storage (localStorage/cookies)
           - Clear Authorization header
           - Redirect to login page
        2. On 400/401 errors:
           - Force client-side token cleanup
           - Redirect to login
        3. On 429 errors:
           - Show retry timer (1 minute)
        """
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response(
                    {'error': 'Missing refresh token in request body'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate and blacklist token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {'message': 'Logout successful. Tokens invalidated.'},
                status=status.HTTP_200_OK
            )

        except Ratelimited:
            return Response(
                {'error': 'Too many requests - try again in 1 minute'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        except TokenError as e:
            return Response(
                {
                    'error': 'Invalid refresh token',
                    'detail': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Log full error details internally
            return Response(
                {
                    'error': 'Logout failed',
                    'detail': 'Please try again or contact support'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )