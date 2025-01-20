
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from products import product_serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from products.product_management import ManageProducts
from system import permissions

# Create your views here.
#product categories
class FetchProductCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):

        product_categories,message = ManageProducts.fetch_product_categories()
        product_category_data = product_serializers.Product_Category_Serializer(product_categories,many=True)
        if product_categories:
            return Response(
                {"message": message,"product_category": product_category_data.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

class FetchProductCategoryWithPkView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,pk,format=None):

        product_category_pk = pk
        product_category,message = ManageProducts.fetch_product_categories(product_category_pk=product_category_pk)
        product_category_data = product_serializers.Product_Category_Serializer(product_category,many=False)
        if product_category:
            return Response(
                {"message": message,"product_category": product_category_data.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

class CreateProductCategoryView(APIView):
   
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

class UpdateProductCategoryView(APIView):

    serializer_class = product_serializers.Product_Category_Serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request,pk, format=None):

        product_category_pk = pk
        product_category_name = self.request.data['category_name']
        product_category_description = self.request.data['description']
        if not product_category_name or not product_category_description:
            return Response(
                {"error": "Both 'name' and 'description' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        updated_product_category, message = ManageProducts.update_product_category(product_category_pk=product_category_pk,new_category_name=product_category_name,description=product_category_description)
        if updated_product_category:
            return Response(
                {"message": message},
                status=status.HTTP_200_OK
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

class DeleteProductCategoryView(APIView):

    serializer_class = product_serializers.Product_Category_Serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,pk,format=None):
        
        product_category_pk = pk
        deleted,message = ManageProducts.delete_product_category(product_category_pk=product_category_pk)
        if deleted:
            return Response(
                {"message": message},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        
#product sub categories
class FetchProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,pk,format=None):

        product_category_pk = pk
        product_sub_categories,message = ManageProducts.fetch_all_product_sub_categories_for_a_category(product_category_pk=product_category_pk)
        product_sub_categories_data = product_serializers.Product_Sub_Category_Serializer(product_sub_categories,many=True)
        if product_sub_categories_data:
            return Response(
                {"message": message,"product_sub_category": product_sub_categories_data.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        
class CreateProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,pk,format=None):

        product_category_pk = pk
        product_sub_category_name = request.data['sub_category_name']
        product_sub_category_description = request.data['description']
        product_sub_category,message = ManageProducts.create_product_sub_category(product_category_pk=product_category_pk,sub_category_name=product_sub_category_name,description=product_sub_category_description)
        if product_sub_category:
            return Response(
                {"message": message},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,pk,format=None):

        product_sub_category_pk = pk
        category_pk_list = request.data['category_pk_list']
        sub_category_name = request.data['sub_category_name']
        description = request.data['description']

        updated_product_sub_category,message = ManageProducts.update_product_sub_category(product_sub_category_pk=product_sub_category_pk,
                                                                                          category_pk_list=category_pk_list,sub_category_name=sub_category_name,
                                                                                          description=description)
        if updated_product_sub_category:
            return Response(
                {"message": message},
                status=status.HTTP_200_OK
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,pk,format=None):

        product_sub_category_pk = pk
        deleted,message = ManageProducts.delete_product_sub_category(product_sub_category_pk=product_sub_category_pk)
        if deleted:
            return Response(
                {"message": message},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

