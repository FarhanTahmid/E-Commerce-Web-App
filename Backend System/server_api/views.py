
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from products import product_serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from products.product_management import ManageProducts
from business_admin.admin_management import AdminManagement
from django.contrib.auth import authenticate, login,logout
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from system.system_log import SystemLogs
# Create your views here.

#business admin
class SignupBusinessAdminUser(APIView):
    
    permission_classes = [AllowAny]
    def post(self,request,format=None):

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

class LoginInBusinessAdminUser(APIView):

    permission_classes = [AllowAny]
    def post(self,request,format=None):

        username = self.request.data.get('username',None)
        password = self.request.data.get('password',None)

        if username == None or password == None:
            return Response(
                {"error": "Username or Password must be provided!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user:
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
        
class LogOutBusinessAdminUser(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self,request,format=None):

        try:
            # Delete the user's token
            user = SystemLogs.get_logged_in_user(request)
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass

        return Response({
            "message": "Successfully logged out.",
            "redirect_url": "/server_api/business_admin/login/"
        }, status=status.HTTP_200_OK)

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

class UpdateProductCategoryView(APIView):

    serializer_class = product_serializers.Product_Category_Serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request,pk, format=None):

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

class DeleteProductCategoryView(APIView):

    serializer_class = product_serializers.Product_Category_Serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,pk,format=None):
        
        product_category_pk = pk
        deleted,message = ManageProducts.delete_product_category(request,product_category_pk=product_category_pk)
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
        
class UpdateProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,pk,format=None):

        product_sub_category_pk = pk
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
        
class DeleteProductSubCategoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,pk,format=None):

        product_sub_category_pk = pk
        deleted,message = ManageProducts.delete_product_sub_category(request,product_sub_category_pk=product_sub_category_pk)
        if deleted:
            return Response(
                {"message": message},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

