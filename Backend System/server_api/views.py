
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from products import product_serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from products.product_management import ManageProducts
from business_admin.admin_management import AdminManagement
from business_admin.serializers import TokenSerializer
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from system.system_log import SystemLogs
from django.contrib.auth.models import User

# Create your views here.

#business admin
class FetchToken(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        try:
            username = self.request.data.get('username',None)
            token,message = AdminManagement.fetch_token(username=username)
            token_data = TokenSerializer(token,many=False)
            if token_data:
                return Response(
                    {"message": message,"token": token_data.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching token."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignupBusinessAdminUser(APIView):
    
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        try:
            admin_full_name = self.request.data.get('admin_full_name',None)
            admin_user_name = self.request.data.get('admin_user_name',None)
            password = self.request.data.get('password',None)
            confirm_password = self.request.data.get('confirm_password',None)
            admin_position_pk = self.request.data.get('admin_position_pk',None)
            admin_contact_no = self.request.data.get('admin_contact_no',None)
            admin_email = self.request.data.get('admin_email',None)
            admin_avatar = self.request.data.get('admin_avatar', None)

            if password != confirm_password:
                return Response(
                    {"error": "Password does not match. Try again!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            business_admin_user,message = AdminManagement.create_business_admin_user(admin_full_name=admin_full_name,admin_user_name=admin_user_name,
                                                                                    password=password,admin_position_pk=admin_position_pk,
                                                                                    admin_contact_no=admin_contact_no,admin_email=admin_email,
                                                                                    admin_avatar=admin_avatar)
            if business_admin_user:
                authenticated_user = authenticate(username=admin_user_name, password=password)
                if authenticated_user:
                    login(request, authenticated_user)
                    return Response(
                        {"message": "Business Admin created successfully. Redirecting to dashboard...", 
                        "redirect_url": "/dashboard"},  # TODO: Provide the dashboard URL
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {"error": "Business Admin created, but login failed. Please log in manually."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"error": message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating Business Admin."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginInBusinessAdminUser(APIView):

    permission_classes = [AllowAny]
    def post(self,request,format=None):
        try:
            username = self.request.data.get('username',None)
            password = self.request.data.get('password',None)

            if username == None or password == None:
                return Response(
                    {"error": "Username or Password must be provided!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user:
                user = User.objects.get(username = username)
                Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)
                token.save()
                login(request, authenticated_user)
                return Response(
                    {"message": "Logged In", 
                    "redirect_url": "/dashboard"},  # TODO: Provide the dashboard URL
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Username or Password incorrect!"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while logging in."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LogOutBusinessAdminUser(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self,request,format=None):

        try:
            # Delete the user's token
            user = SystemLogs.get_logged_in_user(request)
            Token.objects.filter(user=user).delete()
        except Token.DoesNotExist:
            pass

        return Response({
            "message": "Successfully logged out.",
            "redirect_url": "/server_api/business_admin/login/"
        }, status=status.HTTP_200_OK)

#product categories
class FetchProductCategoryView(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = []

    def get(self,request,format=None,*args, **kwargs):
        try:
            pk = request.query_params.get('pk')
            if pk:
                product_categories,message = ManageProducts.fetch_product_categories(product_category_pk=pk)
                product_category_data = product_serializers.Product_Category_Serializer(product_categories,many=False)
            else:
                product_categories,message = ManageProducts.fetch_product_categories(product_category_pk=pk)
                product_category_data = product_serializers.Product_Category_Serializer(product_categories,many=True)
            if product_categories:
                return Response(
                    {"message": message,"product_category": product_category_data.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching product category."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FetchProductCategoryWithPkView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,pk,format=None):
        try:

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
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching product category with this pk."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateProductCategoryView(APIView):
   
    serializer_class = product_serializers.Product_Category_Serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        
        try:

            product_category_name = self.request.data.get('category_name',None)
            product_category_description = self.request.data.get('description',None)
            if not product_category_name or not product_category_description:
                return Response(
                    {"error": "Both 'name' and 'description' are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            product_category, message = ManageProducts.create_product_category(request,product_category_name=product_category_name,description=product_category_description)
            if product_category:
                # product_category_data = products_serializers.Product_Category_Serializer(product_category)
                return Response(
                    {"message": message},#"product_category": product_category_data.data
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating product category."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateProductCategoryView(APIView):

    serializer_class = product_serializers.Product_Category_Serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request,pk, format=None):
        try:

            product_category_pk = pk
            product_category_name = self.request.data.get('category_name',None)
            product_category_description = self.request.data.get('description',None)
            if not product_category_name or not product_category_description:
                return Response(
                    {"error": "Both 'name' and 'description' are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            updated_product_category, message = ManageProducts.update_product_category(request,product_category_pk=product_category_pk,new_category_name=product_category_name,description=product_category_description)
            if updated_product_category:
                return Response(
                    {"message": message},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while updating product category."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteProductCategoryView(APIView):

    serializer_class = product_serializers.Product_Category_Serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,pk,format=None):
        
        try:

            product_category_pk = pk
            deleted,message = ManageProducts.delete_product_category(request,product_category_pk=product_category_pk)
            if deleted:
                return Response(
                    {"message": message},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while deleting product category."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#product sub categories
class FetchProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,pk,format=None):
        try:

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
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching product sub category."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,product_category_pk,format=None):
        try:

            product_category_pk = product_category_pk
            product_sub_category_name = request.data.get('sub_category_name',None)
            product_sub_category_description = request.data.get('description',None)
            product_sub_category,message = ManageProducts.create_product_sub_category(request,product_category_pk=product_category_pk,sub_category_name=product_sub_category_name,description=product_sub_category_description)
            if product_sub_category:
                return Response(
                    {"message": message},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating product sub category."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,product_sub_category_pk,format=None):
        try:

            product_sub_category_pk = product_sub_category_pk
            category_pk_list = request.data.get('category_pk_list',None)
            sub_category_name = request.data.get('sub_category_name',None)
            description = request.data.get('description',None)

            updated_product_sub_category,message = ManageProducts.update_product_sub_category(request,product_sub_category_pk=product_sub_category_pk,
                                                                                            category_pk_list=category_pk_list,sub_category_name=sub_category_name,
                                                                                            description=description)
            if updated_product_sub_category:
                return Response(
                    {"message": message},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while updating product sub category."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,product_sub_category_pk,format=None):
        try:

            product_sub_category_pk = product_sub_category_pk
            deleted,message = ManageProducts.delete_product_sub_category(request,product_sub_category_pk=product_sub_category_pk)
            if deleted:
                return Response(
                    {"message": message},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while deleting product sub category."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#product brands
class FetchProductBrands(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None,*args, **kwargs):

        try:
            pk = request.query_params.get('pk')
            brand_name = request.query_params.get('brand_name')
            if pk:
                product_brands,message = ManageProducts.fetch_product_brand(pk=pk)
                product_brands_data = product_serializers.Product_Brands_Serializer(product_brands,many=False)
            elif brand_name:
                product_brands,message = ManageProducts.fetch_product_brand(brand_name=brand_name)
                product_brands_data = product_serializers.Product_Brands_Serializer(product_brands,many=False)
            else:
                product_brands,message = ManageProducts.fetch_product_brand()
                product_brands_data = product_serializers.Product_Brands_Serializer(product_brands,many=True)
            if product_brands:
                return Response(
                    {"message": message,"product_brands": product_brands_data.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching product brands."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateProductBrands(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        try:
            pass

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating product brands."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
