from django.shortcuts import render
from django.core.exceptions import ValidationError
from products import products_serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from products.product_management import ManageProducts

# Create your views here.
class CreateProductCategoryView(APIView):
    serializer_class = products_serializers.Product_Category_Serializer
    
    def post(self, request, format=None):
        
        product_category_name = self.request.data['category_name']
        product_category_description = self.request.data['description']
        print(product_category_name)
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
