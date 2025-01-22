from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from products.product_management import ManageProducts

class ProductCategoryListView(APIView):
    """
    API endpoint to retrieve all product categories with rate limiting and API key authentication.

    This endpoint fetches all product categories from the database using the `fetch_all_product_categories` method.
    It provides detailed responses and enhanced error handling to ensure the API remains robust and user-friendly.

    Permissions:
        - Requires a valid API key (enforced via HasAPIKey permission class).
        - Rate limited to 10 requests per minute per IP address.

    Methods:
        GET: Fetches and returns all product categories.

    Responses:
        - **200 OK**: Successfully fetched all product categories.
        - **500 Internal Server Error**: An error occurred during the operation, with an appropriate error message.

    Error Handling:
        - Handles errors from the `fetch_all_product_categories` function gracefully and returns user-friendly messages.
        - Logs errors internally for debugging purposes.

    Example Usage:
        Request:
            GET /api/product-categories/

        Response (Success):
        {
            "success": true,
            "message": "Fetched all product categories successfully!",
            "data": [
                {
                    "id": 1,
                    "name": "Electronics",
                    "description": "All kinds of electronic items."
                },
                {
                    "id": 2,
                    "name": "Clothing",
                    "description": "Fashion and apparel."
                }
            ]
        }

        Response (Failure):
        {
            "success": false,
            "message": "An unexpected error occurred! Please try again later."
        }
    """
    permission_classes = [HasAPIKey]

    @method_decorator(ratelimit(key='ip', rate='10/m', method='GET', block=True))
    def get(self, request):
        """
        Handles GET requests to retrieve all product categories.

        Returns:
            Response: A JSON response containing the product categories or an error message.
        """
        try:
            # Fetch all product categories
            product_categories, message = ManageProducts.fetch_all_product_categories()

            if product_categories:
                # Serialize the product categories
                categories_data = [
                    {
                        "id": category.pk,
                        "name": category.category_name,
                        "description": category.description,
                    }
                    for category in product_categories
                ]
                return Response(
                    {
                        "success": True,
                        "message": message,
                        "data": categories_data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Handle case where no categories are found
                return Response(
                    {
                        "success": False,
                        "message": message,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            # Log the unexpected error (optional, requires a logging setup)
            print(f"Unexpected error in ProductCategoryList API: {str(e)}")

            # Handle unexpected errors gracefully
            return Response(
                {
                    "success": False,
                    "message": "An unexpected error occurred! Please try again later.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )