
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
            
            if ' ' in admin_user_name:
                return Response(
                    {
                        "error": "Admin user name should not contain spaces."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            missing_fields = []
            if not admin_full_name:
                missing_fields.append('admin full name')
            if not admin_user_name:
                missing_fields.append('admin user name')
            if not password:
                missing_fields.append('password')
            if not confirm_password:
                missing_fields.append('confirm password')
            if not admin_position_pk:
                missing_fields.append('admin position')

            if missing_fields:
                return Response(
                    {
                        "error": f"The following fields are required: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

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
                # authenticated_user = authenticate(username=admin_user_name, password=password)
                # if authenticated_user:
                #     login(request, authenticated_user)
                #     return Response(
                #         {"message": "Business Admin created successfully. Redirecting to dashboard...", 
                #         "redirect_url": "/dashboard"},  # TODO: Provide the dashboard URL
                #         status=status.HTTP_201_CREATED
                #     )
                # else:
                #     return Response(
                #         {"error": "Business Admin created, but login failed. Please log in manually."},
                #         status=status.HTTP_400_BAD_REQUEST
                #     )
                return Response(
                        {"message": "Business Admin created successfully. Redirecting to dashboard...", 
                        "redirect_url": "/dashboard"},  # TODO: Provide the dashboard URL
                        status=status.HTTP_201_CREATED)
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

class UpdateBusinessAdminUser(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,admin_user_name,format=None):

        try:
            admin_user_name = admin_user_name
            admin_full_name = self.request.data.get('admin_full_name',None)
            admin_position_pk = self.request.data.get('admin_position_pk',None)
            admin_unique_id = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)[0].admin_unique_id

            #can none
            admin_contact_no = self.request.data.get('admin_contact_no',None)
            admin_email = self.request.data.get('admin_email',None)
            admin_avatar = self.request.data.get('admin_avatar',None)
            old_password = self.request.data.get('old_password',None)
            password = self.request.data.get('password',None)

            missing_fields = []
            if not admin_full_name:
                missing_fields.append("Admin full name")
            if not admin_position_pk:
                missing_fields.append("Admin position")
            if missing_fields:
                return Response(
                    {
                        "error": f"The following fields are required: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            admin_updated ,message = AdminManagement.update_business_admin_user(request,admin_unique_id,admin_full_name,admin_position_pk,
                                                                                admin_contact_no,admin_email,admin_avatar,old_password,password,admin_user_name)
            if admin_updated:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'message':message
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while updating business admin user"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateBusinessAdminUserPassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,admin_user_name,format=None):
        try:

            admin_user_name = admin_user_name
            admin_unique_id = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)[0].admin_unique_id
            old_password = self.request.data.get('old_password',None)
            new_password = self.request.data.get('new_password',None)
            new_password_confirm = self.request.data.get('new_password_confirm',None)

            if not new_password or not new_password_confirm:
                return Response({
                    'error':"Please provide new password"
                },status=status.HTTP_400_BAD_REQUEST)
            if not old_password:
                return Response({
                    'error':"Please provide old password"
                },status=status.HTTP_400_BAD_REQUEST)
            if new_password == new_password_confirm:
                password_update,message = AdminManagement.update_business_admin_user_password(request,admin_unique_id,old_password,new_password)

                if password_update:
                    return Response({
                        'message':message
                    },status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error':message
                    },status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error':"Password does not match"
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while updating business admin user password"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteBusinessAdminUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,admin_user_name,format=None):
        try:
            admin_user_name=admin_user_name
            admin_unique_id = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)[0].admin_unique_id
            deleted,message = AdminManagement.delete_business_admin_user(request,admin_unique_id)
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
                "message": "An error occurred while deleting business admin user"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


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

            missing_fields = []
            if not product_category_name:
                missing_fields.append("Product category name")
            if not product_category_description:
                missing_fields.append("Product category description")
            
            if missing_fields:
                return Response(
                    {
                        "error": f"The following fields are required: {', '.join(missing_fields)}"
                    },
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
            missing_fields = []
            if not product_category_name:
                missing_fields.append("Product category name")
            if not product_category_description:
                missing_fields.append("Product category description")
            if missing_fields:
                return Response(
                    {
                        "error": f"The following fields are required: {', '.join(missing_fields)}"
                    },
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
            missing_fields = []
            if not product_sub_category_name:
                missing_fields.append("Product Sub Category name")
            if not product_sub_category_description:
                missing_fields.append("Product Sub Category description")
            if missing_fields:
                return Response(
                    {
                        "error": f"The following fields are required: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
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
            missing_fields = []
            if not category_pk_list:
                missing_fields.append("Product Categories")
            if not sub_category_name:
                missing_fields.append("Product Sub Category name")
            if not description:
                missing_fields.append("Product Sub Category descrpition")
            if missing_fields:
                return Response(
                    {
                        "error": f"The following fields are required: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
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
            
            brand_name = self.request.data.get('brand_name',None)
            brand_established_year = self.request.data.get('brand_established_year',None)
            is_own_brand = self.request.data.get('is_own_brand',False)
            brand_country = self.request.data.get('brand_country',None)
            brand_description = self.request.data.get('brand_description',None)
            brand_logo = self.request.data.get('brand_logo',None)

            missing_fields = []
            if not brand_name:
                missing_fields.append("Brand name")
            if not brand_established_year:
                missing_fields.append("Brand established year")
            if missing_fields:
                return Response(
                    {
                        "error": f"The following fields are required: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            product_brand,message = ManageProducts.create_product_brand(request,brand_name,brand_established_year,is_own_brand,
                                                                        brand_country,brand_description,brand_logo)
            if product_brand:
                return Response(
                    {
                        "message": "Brand created"
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating product brand."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateProductBrands(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,product_brand_pk,format=None):
        try:
            product_brand_pk = product_brand_pk
            brand_name = self.request.data.get('brand_name',None)
            brand_established_year = self.request.data.get('brand_established_year',None)
            is_own_brand = self.request.data.get('is_own_brand',False)
            brand_country = self.request.data.get('brand_country',None)
            brand_description = self.request.data.get('brand_description',None)
            brand_logo = self.request.data.get('brand_logo',None)

            missing_fields = []
            if not brand_name:
                missing_fields.append("Product Brand name")
            if not brand_established_year:
                missing_fields.append("PRoduct Brand established year")
            if missing_fields:
                return Response(
                    {
                        "error": f"The following fields are required: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            product_brand_update,message = ManageProducts.update_product_brand(request,product_brand_pk,brand_name,brand_established_year,
                                                                               is_own_brand,brand_country,brand_description,brand_logo)

            if product_brand_update:
                return Response(
                    {
                        "message": "Brand updated"
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while updating product brand."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteProductBrands(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,product_brand_pk,format=None):
        try:

            product_brand_pk=product_brand_pk
            deleted,message= ManageProducts.delete_product_brand(request,product_brand_pk)
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
                "message": "An error occurred while updating product brand."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#product flavour
class FetchProductFlavour(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None,*args, **kwargs):
        try:
            pk = request.query_params.get('pk')
            product_flavour_name = request.query_params.get('product_flavour_name')

            if pk:
                product_flavours,message = ManageProducts.fetch_product_flavour(pk=pk)
                product_flavours_data = product_serializers.Product_Flavour_Serializer(product_flavours,many=False)
            elif product_flavour_name:
                product_flavours,message = ManageProducts.fetch_product_flavour(product_flavour_name=product_flavour_name)
                product_flavours_data = product_serializers.Product_Flavour_Serializer(product_flavours,many=False)
            else:
                product_flavours,message = ManageProducts.fetch_product_flavour()
                product_flavours_data = product_serializers.Product_Flavour_Serializer(product_flavours,many=True)
            
            if product_flavours:
                return Response(
                    {"message": message,"product_flavours_data":product_flavours_data.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching product flavour."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateProductFlavour(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):

        try:
            product_flavour_name = self.request.data.get('product_flavour_name',None)
            if not product_flavour_name:
                return Response(
                    {
                        'error':'Product flavour name required'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            product_flavour,message = ManageProducts.create_product_flavour(request,product_flavour_name)
            if product_flavour:
                return Response({
                    'message':message
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating product flavour."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateProductFlavour(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,product_flavour_pk,format=None):
        try:
            product_flavour_pk=product_flavour_pk
            product_flavour_name = self.request.data.get('product_flavour_name',None)
            if not product_flavour_name:
                return Response({
                    'error':"Product flavour name required"
                },status=status.HTTP_400_BAD_REQUEST)
            
            product_flavour_updated,message = ManageProducts.update_product_flavour(request,product_flavour_pk,product_flavour_name)
            if product_flavour_updated:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while updating product flavour."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteProductFlavour(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,product_flavour_pk,format=None):
        try:
            product_flavour_pk = product_flavour_pk
            deleted,message = ManageProducts.delete_product_flavour(request,product_flavour_pk=product_flavour_pk)
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
                "message": "An error occurred while deleting product flavour."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#product
class FetchProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None,*args, **kwargs):
        try:

            product_pk = self.request.data.get('product_pk',None)
            product_name = self.request.data.get('product_name',None)
            product_brand_pk = self.request.data.get('product_brand_pk',None)
            product_category_pk_list = self.request.data.get('product_category_pk_list',None)
            product_sub_category_pk_list = self.request.data.get('product_sub_category_pk_list',None)

            if product_pk:
                product,message = ManageProducts.fetch_product(product_pk=product_pk)
                product_data = product_serializers.Product_Serializer(product,many=False)
            elif product_name:
                product,message = ManageProducts.fetch_product(product_name=product_name)
                product_data = product_serializers.Product_Serializer(product,many=False)
            elif product_brand_pk:
                product,message = ManageProducts.fetch_product(product_brand_pk=product_brand_pk)
                product_data = product_serializers.Product_Serializer(product,many=False)
            elif product_category_pk_list:
                product,message = ManageProducts.fetch_product(product_category_pk_list=product_category_pk_list)
                product_data = product_serializers.Product_Serializer(product,many=True)
            elif product_sub_category_pk_list:
                product,message = ManageProducts.fetch_product(product_sub_category_pk_list=product_sub_category_pk_list)
                product_data = product_serializers.Product_Serializer(product,many=True)
            else:
                product,message = ManageProducts.fetch_product()
                product_data = product_serializers.Product_Serializer(product,many=True)
            
            if product:
                return Response({
                    'message':message,
                    'product_data':product_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching product."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        try:

            product_name = self.request.data.get('product_name',None)
            product_category_pk_list = self.request.data.get('product_category_pk_list',None)
            product_sub_category_pk_list = self.request.data.get('product_sub_category_pk_list',None)
            product_description = self.request.data.get('product_description',None)
            product_summary = self.request.data.get('product_summary',None)
            

            #can none
            product_brand_pk = self.request.data.get('product_brand_pk',None)
            product_ingredients = self.request.data.get('product_ingredients',None)
            product_usage_direction = self.request.data.get('product_usage_direction',None)

            missing_fields = []
            if not product_name:
                missing_fields.append("Product Name")
            if not product_category_pk_list:
                missing_fields.append("Product Categories")
            if not product_sub_category_pk_list:
                missing_fields.append("Product Sub Categories")
            if not product_description:
                missing_fields.append("Product Description")
            if not product_summary:
                missing_fields.append("Product Summary")
            
            if missing_fields:
                return Response({
                    'error':f"The following fields are required: {', '.join(missing_fields)}"
                },status=status.HTTP_400_BAD_REQUEST)
            
            product_created,message = ManageProducts.create_product(request,product_name,product_category_pk_list,product_sub_category_pk_list,
                                                                    product_description,product_summary,product_brand_pk,
                                                                    product_ingredients,product_usage_direction)
            if product_created:
                return Response({
                    'message':message
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating product."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,product_pk,format=None):
    
        try:
            product_pk = product_pk
            product_name = self.request.data.get('product_name',None)
            product_category_pk_list = self.request.data.get('product_category_pk_list',None)
            product_sub_category_pk_list = self.request.data.get('product_sub_category_pk_list',None)
            product_description = self.request.data.get('product_description',None)
            product_summary = self.request.data.get('product_summary',None)

            #can none
            product_brand_pk = self.request.data.get('product_brand_pk',None)
            product_ingredients = self.request.data.get('product_ingredients',None)
            product_usage_direction = self.request.data.get('product_usage_direction',None)

            missing_fields = []
            if not product_name:
                missing_fields.append("Product Name")
            if not product_category_pk_list:
                missing_fields.append("Product Categories")
            if not product_sub_category_pk_list:
                missing_fields.append("Product Sub Categories")
            if not product_description:
                missing_fields.append("Product Description")
            if not product_summary:
                missing_fields.append("Product Summary")
            
            if missing_fields:
                return Response({
                    'error':f"The following fields are required: {', '.join(missing_fields)}"
                },status=status.HTTP_400_BAD_REQUEST)
            
            product_update,message = ManageProducts.update_product(request,product_pk,product_name,product_category_pk_list,product_sub_category_pk_list,
                                                                   product_description,product_summary,product_brand_pk,
                                                                   product_ingredients,product_usage_direction)
            if product_update:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while updating product."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,product_pk,format=None):

        try:
            product_pk = product_pk
            deleted ,message = ManageProducts.delete_product(request,product_pk)
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
                "message": "An error occurred while deleting product."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#product sku
class FetchProductSKU(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None,*args, **kwargs):
        try:

            pk = self.request.query_params.get('pk',None)
            product_id = self.request.query_params.get('product_id',None)
            product_name = self.request.query_params.get('product_name',None)
            product_sku = self.request.query_params.get('product_sku',None)

            if pk:
                product_sku_fetch,message = ManageProducts.fetch_product_sku(pk=pk)
                product_sku_fetch_data = product_serializers.Product_SKU_Serializer(product_sku_fetch,many=False)
            elif product_id:
                product_sku_fetch,message = ManageProducts.fetch_product_sku(product_id=product_id)
                product_sku_fetch_data = product_serializers.Product_SKU_Serializer(product_sku_fetch,many=False)
            elif product_name:
                product_sku_fetch,message = ManageProducts.fetch_product_sku(product_name=product_name)
                product_sku_fetch_data = product_serializers.Product_SKU_Serializer(product_sku_fetch,many=False)
            elif product_sku:
                product_sku_fetch,message = ManageProducts.fetch_product_sku(product_sku=product_sku)
                product_sku_fetch_data = product_serializers.Product_SKU_Serializer(product_sku_fetch,many=False)
            else:
                return Response({
                    'error': "No parameter passed! Must pass a single parameter"
                },status=status.HTTP_400_BAD_REQUEST)
            
            if product_sku_fetch:
                return Response({
                    'message':message,
                    'product_sku_fetch':product_sku_fetch_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching product sku."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateProductSKU(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):

        try:
            product_pk = self.request.data.get('product_pk',None)
            product_price = self.request.data.get('product_price',None)
            product_stock = self.request.data.get('product_stock',None)
            product_flavours_pk_list = self.request.data.get('product_flavours_pk_list',None)

            #can none
            product_color = self.request.data.get('product_color',None)
            product_size = self.request.data.get('product_size',None)

            missing_fields = []
            if not product_pk:
                missing_fields.append("Product")
            if not product_price:
                missing_fields.append("Price")
            if not product_stock:
                missing_fields.append("Product stock")
            if not product_flavours_pk_list:
                missing_fields.append("Product Flavours")
            if missing_fields:
                return Response({
                    'error':f"The following fields are required: {', '.join(missing_fields)}"
                },status=status.HTTP_400_BAD_REQUEST)

            product_sku_created,message = ManageProducts.create_product_sku(request,product_pk,product_price,product_stock,product_flavours_pk_list,product_color
                                                                            ,product_size)
            if product_sku_created:
                return Response({
                    'message':message
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating product sku."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateProductSKU(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,product_sku_pk,format=None):
        try:

            product_sku_pk=product_sku_pk
            product_id = self.request.data.get('product_id',None)
            product_price = self.request.data.get('product_price',None)
            product_stock = self.request.data.get('product_stock',None)
            product_flavours_pk_list = self.request.data.get('product_flavours_pk_list',None)

            #can none
            product_color = self.request.data.get('product_color',None)
            product_size = self.request.data.get('product_size',None)

            missing_fields = []
            if not product_id:
                missing_fields.append("Product")
            if not product_price:
                missing_fields.append("Price")
            if not product_stock:
                missing_fields.append("Product stock")
            if not product_flavours_pk_list:
                missing_fields.append("Product Flavours")
            if missing_fields:
                return Response({
                    'error':f"The following fields are required: {', '.join(missing_fields)}"
                },status=status.HTTP_400_BAD_REQUEST)

            product_sku_update, message = ManageProducts.update_product_sku(request,product_sku_pk,product_id,product_price,
                                                                            product_stock,product_flavours_pk_list,product_color,product_size)
            if product_sku_update:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while updating product sku."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
class DeleteProductSKU(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,product_sku_pk,format=None):
        try:
            product_sku_pk = product_sku_pk
            deleted,message = ManageProducts.delete_product_sku(request,product_sku_pk)
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
                "message": "An error occurred while deleting product sku."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
#product image
class FetchProductImages(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None,*args, **kwargs):
        try:
            product_pk = self.request.query_params.get('product_pk',None)
            product_image_pk = self.request.query_params.get('product_image_pk',None)
            if product_pk:
                product_images,message = ManageProducts.fetch_product_image(product_pk=product_pk)
                product_images_data = product_serializers.Product_Images_Serializer(product_images,many=True)
            elif product_image_pk:
                product_images,message = ManageProducts.fetch_product_image(product_image_pk=product_image_pk)
                product_images_data = product_serializers.Product_Images_Serializer(product_images,many=False)
            else:
                product_images,message = ManageProducts.fetch_product_image()
                product_images_data = product_serializers.Product_Images_Serializer(product_images,many=True)
            
            if product_images:
                return Response({
                    'message':message,
                    'product_image_data':product_images_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching product image."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
class CreateProductImages(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,product_id,format=None):
        try:
            product_id=product_id
            product_image_list = self.request.data.getlist('product_image_list',None)#as multiform data need to use getlist
            #can none
            color = self.request.data.get('color',None)
            size = self.request.data.get('size',None)


            if not product_image_list:
                return Response({
                    'error':'Please select atleast 1 image'
                },status=status.HTTP_400_BAD_REQUEST)

            product_images,message = ManageProducts.create_product_image(request,product_id,product_image_list,color,size)
            if product_images:
                return Response({
                    'message':message
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating product image."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
class UpdateProductImage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,product_image_pk,format=None):
        try:
            product_image_pk=product_image_pk

            #can none
            new_image = self.request.data.get('new_image',None)
            color = self.request.data.get('color',None)
            size = self.request.data.get('size',None)

            product_image_updated,message = ManageProducts.update_product_image(request,product_image_pk,new_image,color,size)
            if product_image_updated:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while updating product image."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
class DeleteProductImage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,product_image_pk,format=None):
        try:
            product_image_pk = product_image_pk
            deleted,message = ManageProducts.delete_product_image(request,product_image_pk)
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
                "message": "An error occurred while deleting image."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
class FetchProductDiscount(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None,*args, **kwargs):
        try:
            
            product_id = self.request.query_params.get('product_id',None)
            discount_name = self.request.query_params.get('discount_name',None)
            is_active = self.request.query_params.get('is_active',None)
            product_discount_pk = self.request.query_params.get('product_discount_pk',None)

            if product_id:
                product_discount,message = ManageProducts.fetch_product_discount(product_id=product_id)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif discount_name:
                product_discount,message = ManageProducts.fetch_product_discount(discount_name=discount_name)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=False)
            elif is_active:
                product_discount,message = ManageProducts.fetch_product_discount(is_active=True)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif product_discount_pk:
                product_discount,message = ManageProducts.fetch_product_discount(product_discount_pk=product_discount_pk)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=False)
            else:
                product_discount,message = ManageProducts.fetch_product_discount()
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            
            if product_discount:
                return Response({
                    'message':message,
                    'product_discount':product_discount_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while fetching product discount."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
class CreateProductDiscount(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,product_id,format=None):

        try:
            product_id = product_id
            discount_name = self.request.query_params.get('discount_name',None)
            discount_amount = self.request.query_params.get('discount_amount',None)
            start_date = self.request.query_params.get('start_date',None)
            end_date = self.request.query_params.get('end_date',None)
            if start_date>end_date:
                return Response({
                    'error':"Start date of dicount must be less than or equal to end data"
                },status=status.HTTP_400_BAD_REQUEST)
            discount_created,message = ManageProducts.create_product_discount(request,product_id,discount_name,discount_amount,start_date,end_date)
            if discount_created:
                return Response({
                    'messge':message
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e),
                "message": "An error occurred while creating product discount."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 