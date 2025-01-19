from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from products import product_serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from products.product_management import ManageProducts

# Create your views here.
class CreateProductCategoryView(APIView):
   
    """
    API view to create a new product category.

    This view handles the creation of a new product category. It expects the request data to contain
    the category name and description. If either of these fields is missing, it returns a 400 Bad Request response.
    If the category is created successfully, it returns a 201 Created response with a success message.
    If there is an error during the creation process, it returns a 400 Bad Request response with an error message.

    Attributes:
        serializer_class (Serializer): The serializer class used for validating and serializing the product category data.

    Methods:
        post(request, format=None):
            Handles the POST request to create a new product category.

    Example Usage:
        POST /api/product-categories/
        {
            "category_name": "Skincare",
            "description": "Products for skincare"
        }

        Response (201 Created):
        {
            "message": "Product category created successfully!"
        }

        Response (400 Bad Request):
        {
            "error": "Both 'name' and 'description' are required."
        }

        Response (400 Bad Request):
        {
            "error": "An unexpected error occurred while creating the product category. Please try again later."
        }
    """

    serializer_class = product_serializers.Product_Category_Serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        
        product_category_name = self.request.data['category_name']
        product_category_description = self.request.data['description']
        if not product_category_name or not product_category_description:
            return Response(
                {"error": "Both 'name' and 'description' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        product_category, message = ManageProducts.create_product_category(product_category_name=product_category_name,description=product_category_description)
        if product_category:
            # product_category_data = products_serializers.Product_Category_Serializer(product_category)
            return Response(
                {"message": message},#"product_category": product_category_data.data
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
