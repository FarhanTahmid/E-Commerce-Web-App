
from rest_framework.permissions import IsAuthenticated
from products import product_serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from products.product_management import ManageProducts
from business_admin.admin_management import AdminManagement
from rest_framework.permissions import AllowAny
from json.decoder import JSONDecodeError
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.exceptions import Ratelimited
from system.models import *
from business_admin import serializers
from system.permissions import IsAdminWithPermission
from business_admin.models import *
from e_commerce_app.settings import MEDIA_URL
from datetime import datetime

REFRESH_RATE = '50/m'
SERVER_API_URL = 'server_api'

# Create your views here.

#business admin
class SignupBusinessAdminUser(APIView):
    
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):
        try:
            admin_full_name = self.request.data.get('admin_full_name',"")
            admin_email = self.request.data.get('admin_email',"")
            password = self.request.data.get('password',"")
            confirm_password = self.request.data.get('confirm_password',"")

            admin_contact_no = self.request.data.get('admin_contact_no',"")
            admin_avatar = self.request.data.get('admin_avatar',"")
            is_superuser = self.request.data.get('is_superuser',False)
            is_staff = self.request.data.get('is_superuser',False)
            

            missing_fields = []
            if admin_full_name == "":
                missing_fields.append('admin full name')
            if admin_email == "":
                missing_fields.append('admin email')
            if password == "":
                missing_fields.append('password')
            if confirm_password == "":
                missing_fields.append('confirm password')

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
            
            business_admin_user,message = AdminManagement.create_business_admin_user(admin_full_name=admin_full_name,
                                                                                    password=password,
                                                                                    admin_contact_no=admin_contact_no,admin_email=admin_email,
                                                                                    admin_avatar=admin_avatar,is_superuser=is_superuser,is_staff_user=is_staff)
            if business_admin_user:
                return Response({
                    'message':"Business Admin created successfully. Redirecting to login page",
                    "redirect_url": "/login-page"
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
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

class LoginInBusinessAdminUser(APIView):

    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):
        try:
            email = self.request.data.get('email',"")
            password = self.request.data.get('password',"")

            if email == "" or password == "":
                return Response(
                    {"error": "Email or Password must be provided!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            authenticated_user = authenticate(email=email, password=password)
            if authenticated_user:
                refresh=RefreshToken.for_user(authenticated_user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'Login successful',
                    'redirect_url': 'dashoard-link/',
                    'username': authenticated_user.username,
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
        
class LogOutBusinessAdminUser(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):

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
                {'message': 'Logout successful. Tokens invalidated.',
                 'redirect_url':'/server_api/business_admin/login/'},
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

class UpdateBusinessAdminUser(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,admin_user_name,format=None):

        try:
            admin_user_name = admin_user_name
            admin_full_name = self.request.data.get('admin_full_name',"")
            admin_email = self.request.data.get('admin_email',"")
            #can none
            admin_contact_no = self.request.data.get('admin_contact_no',"")
            admin_avatar = self.request.data.get('admin_avatar',"")
            old_password = self.request.data.get('old_password',"")
            password = self.request.data.get('password',"")
            is_superuser = self.request.data.get('is_superuser',False)
            is_staff_user = self.request.data.get('is_staff_user',False)
            missing_fields = []
            if admin_full_name == "":
                missing_fields.append("Admin full name")
            if missing_fields:
                return Response(
                    {
                        "error": f"The following fields are required: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            admin_updated ,message = AdminManagement.update_business_admin_user(request,admin_user_name,admin_full_name,
                                                                                admin_email,admin_contact_no,admin_avatar,old_password,password,is_superuser,is_staff_user)
            if admin_updated:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'message':message
                },status=status.HTTP_400_BAD_REQUEST)
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
        
class UpdateBusinessAdminUserPassword(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,admin_user_name,format=None):
        try:

            admin_user_name = admin_user_name
            old_password = self.request.data.get('old_password',"")
            new_password = self.request.data.get('new_password',"")
            new_password_confirm = self.request.data.get('new_password_confirm',"")
            if new_password == "" or new_password_confirm == "":
                return Response({
                    'error':"Please provide new password"
                },status=status.HTTP_400_BAD_REQUEST)
            if not old_password or old_password == "":
                return Response({
                    'error':"Please provide old password"
                },status=status.HTTP_400_BAD_REQUEST)
            if new_password == new_password_confirm:
                password_update,message = AdminManagement.update_business_admin_user_password(request,admin_user_name,old_password,new_password)
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
        
class DeleteBusinessAdminUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
    def delete(self,request,admin_user_name,format=None):
        try:
            admin_user_name=admin_user_name
            admin = Accounts.objects.get(username = admin_user_name)
            admin_unique_id = AdminManagement.fetch_business_admin_user(admin_email=admin.email)[0].admin_unique_id
            deleted,message = AdminManagement.delete_business_admin_user(request,admin_unique_id)
            if deleted:
                return Response(
                    {"message": message},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
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
        
class FetchBusinessAdminUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None):
        try:
            
            admin_unique_id = self.request.query_params.get('admin_unique_id',"")
            admin_email = self.request.query_params.get('admin_email',"")
            admin_user_name = self.request.query_params.get('admin_user_name',"")

            if admin_unique_id != "":
                fetched_admin,message = AdminManagement.fetch_business_admin_user(admin_unique_id=admin_unique_id)
                fetched_admin_data = serializers.BusinessAdminUserSerializer(fetched_admin,many=False)
            elif admin_email!= "":
                fetched_admin,message = AdminManagement.fetch_business_admin_user(admin_email=admin_email)
                fetched_admin_data = serializers.BusinessAdminUserSerializer(fetched_admin,many=False)
            elif admin_user_name!= "":
                fetched_admin,message = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)
                fetched_admin_data = serializers.BusinessAdminUserSerializer(fetched_admin,many=False)
            else:
                fetched_admin,message = AdminManagement.fetch_business_admin_user()
                fetched_admin_data = serializers.BusinessAdminUserSerializer(fetched_admin,many=True)

            if fetched_admin:
                return Response({
                    'message':message,
                    'admin_users':fetched_admin_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
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

class FetchBusinessAdminAvatar(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,admin_user_name,format=None):
        try:
            domain = request.get_host()
            admin_user_name = admin_user_name

            if admin_user_name!= "":
                fetched_admin_avatar,message = AdminManagement.fetch_business_admin_profile_picture(admin_user_name=admin_user_name)
            else:
                return Response({
                    'error':"Please provide admin unique id or email or admin user name"
                },status=status.HTTP_400_BAD_REQUEST)
            
            if fetched_admin_avatar:
                return Response({
                    'message':message,
                    'admin_avatar': str(domain)+ '/' + SERVER_API_URL + MEDIA_URL + str(fetched_admin_avatar)
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
            
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

#business admin position

class FetchBusinessAdminPosition(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):
        try:

            name = self.request.query_params.get('name',"")
            pk = self.request.query_params.get('pk',"")
            available = self.request.query_params.get('available',False)

            if name!= "":
                fetched_position,message = AdminManagement.fetch_admin_position(name=name)
                fetched_position_data = serializers.AdminPositionSerializer(fetched_position,many=False)
            elif pk!= "":
                fetched_position,message = AdminManagement.fetch_admin_position(pk=pk)
                fetched_position_data = serializers.AdminPositionSerializer(fetched_position,many=False)
            elif available:
                fetched_position,message = AdminManagement.fetch_admin_position(available=True)
                fetched_position_data = serializers.AdminPositionSerializer(fetched_position,many=True)
            else:
                fetched_position,message = AdminManagement.fetch_admin_position()
                fetched_position_data = serializers.AdminPositionSerializer(fetched_position,many=True)

            if fetched_position:
                return Response({
                    'message':message,
                    'admin_positions':fetched_position_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
            
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
        
class CreateBusinessAdminPosition(APIView):

    """Permissions"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    required_permissions = [
        AdminPermissions.CREATE,
        AdminPermissions.VIEW
    ] 
    def get_permissions(self):
        return [IsAdminWithPermission(self.required_permissions)]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None,*args, **kwargs):
        try:
            name = self.request.data.get('name',"")
            description = self.request.data.get('description',"")

            if name == "":
                return Response({
                    'error':"Admin position name is required"
                },status=status.HTTP_400_BAD_REQUEST)
            
            admin_position_created,message = AdminManagement.create_admin_position(request,name,description)
            if admin_position_created:
                return Response({
                    'message':message
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
            
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

class UpdateBusinessAdminPosition(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,admin_position_pk,format=None,*args, **kwargs):
        try:
            admin_position_pk= admin_position_pk
            name = self.request.data.get('name',"")
            description = self.request.data.get('description',"")
            if name == "":
                return Response({
                    'message':"Admin position name is required"
                },status=status.HTTP_400_BAD_REQUEST)
            admin_position_updated,message = AdminManagement.update_admin_position(request,admin_position_pk,name,description)
            if admin_position_updated:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

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

class DeleteBusinessAdminPosition(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def delete(self,request,admin_position_pk,format=None,*args, **kwargs):

        try:
            admin_position_pk =admin_position_pk
            deleted,message = AdminManagement.delete_admin_position(request,admin_position_pk)
            if deleted:
                return Response(
                    {"message": message},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

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

#business admin permission
class FetchBusinessAdminPermission(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):
        try:
            permission_pk = self.request.query_params.get('permission_pk',"")
            permission_name = self.request.query_params.get('permission_name',"")

            if permission_pk != "":
                admin_permission,message = AdminManagement.fetch_admin_permissions(permission_pk=permission_pk)
                admin_permission_data = serializers.AdminPermissionSerializer(admin_permission,many=False)
            elif permission_name!= "":
                admin_permission,message = AdminManagement.fetch_admin_permissions(permission_name=permission_name)
                admin_permission_data = serializers.AdminPermissionSerializer(admin_permission,many=False)
            else:
                admin_permission,message = AdminManagement.fetch_admin_permissions()
                admin_permission_data = serializers.AdminPermissionSerializer(admin_permission,many=True)
            
            if admin_permission:
                return Response({
                    'message':message,
                    'admin_permission':admin_permission_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
            
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

class CreateBusinessAdminPermission(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None,*args, **kwargs):
        try:

            permission_name = self.request.data.get('permission_name',"")
            permission_description = self.request.data.get('permission_description',"")

            if permission_name == "":
                return Response({
                    'error':'Permission name required'
                },status=status.HTTP_400_BAD_REQUEST)
            
            permission_created,message = AdminManagement.create_admin_permissions(request,permission_name,permission_description)
            if permission_created:
                return Response({
                    'message':message
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

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
        
class UpdateBusinessAdminPermission(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,admin_permission_pk,format=None,*args, **kwargs):

        try:
            admin_permission_pk=admin_permission_pk
            permission_name = self.request.data.get('permission_name',"")
            permission_description = self.request.data.get('permission_description',"")

            if permission_name == "":
                return Response({
                    'error':'Permission name required'
                },status=status.HTTP_400_BAD_REQUEST)
            
            updated_permission,message = AdminManagement.update_admin_permissions(request,admin_permission_pk,permission_name,permission_description)
            if updated_permission:
                return Response({
                    'message':message,
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

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
        
class DeleteBusinessAdminPermission(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
    def delete(self,request,admin_permission_pk,format=None,*args, **kwargs):

        try:

            admin_permission_pk = admin_permission_pk
            deleted,message = AdminManagement.delete_admin_permissions(request,admin_permission_pk)
            if deleted:
                return Response(
                    {"message": message},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

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

#product categories
class FetchProductCategoryView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):
        try:
            pk = request.query_params.get('pk',"")
            if pk!= "":
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

class FetchProductCategoryWithPkView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
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

class CreateProductCategoryView(APIView):
   
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self, request, format=None):
        
        try:

            product_category_name = self.request.data.get('category_name',"")
            product_category_description = self.request.data.get('description',"")

            missing_fields = []
            if product_category_name == "":
                missing_fields.append("Product category name")
            if product_category_description == "":
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

class UpdateProductCategoryView(APIView):

    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self, request,pk, format=None):
        try:

            product_category_pk = pk
            product_category_name = self.request.data.get('category_name',"")
            product_category_description = self.request.data.get('description',"")
            missing_fields = []
            if  product_category_name == "":
                missing_fields.append("Product category name")
            if product_category_description == "":
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

class DeleteProductCategoryView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
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
        
#product sub categories
class FetchProductSubCategoryView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
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
        
class CreateProductSubCategoryView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,product_category_pk,format=None):
        try:

            product_category_pk = product_category_pk
            product_sub_category_name = request.data.get('sub_category_name',"")
            product_sub_category_description = request.data.get('description',"")
            missing_fields = []
            if product_sub_category_name=="":
                missing_fields.append("Product Sub Category name")
            if product_sub_category_description == "":
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
        
class UpdateProductSubCategoryView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,product_sub_category_pk,format=None):
        try:

            product_sub_category_pk = product_sub_category_pk
            category_pk_list = request.data.get('category_pk_list',[])
            sub_category_name = request.data.get('sub_category_name',"")
            description = request.data.get('description',"")
            missing_fields = []
            if len(category_pk_list) == 0 :
                missing_fields.append("Product Categories")
            if sub_category_name == "":
                missing_fields.append("Product Sub Category name")
            if description == "":
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
        
class DeleteProductSubCategoryView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
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
        
#product brands
class FetchProductBrands(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):

        try:
            pk = request.query_params.get('pk',"")
            brand_name = request.query_params.get('brand_name',"")
            if pk!= "":
                product_brands,message = ManageProducts.fetch_product_brand(pk=pk)
                product_brands_data = product_serializers.Product_Brands_Serializer(product_brands,many=False,context={'request': request})
            elif brand_name!= "":
                product_brands,message = ManageProducts.fetch_product_brand(brand_name=brand_name)
                product_brands_data = product_serializers.Product_Brands_Serializer(product_brands,many=False,context={'request': request})
            else:
                product_brands,message = ManageProducts.fetch_product_brand()
                product_brands_data = product_serializers.Product_Brands_Serializer(product_brands,many=True,context={'request': request})
            if product_brands:
                return Response(
                    {"message": message,"product_brands": product_brands_data.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

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
        
class CreateProductBrands(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):
        try:
            
            brand_name = self.request.data.get('brand_name',"")
            brand_established_year = self.request.data.get('brand_established_year',"")
            is_own_brand = self.request.data.get('is_own_brand',False)
            brand_country = self.request.data.get('brand_country',"")
            brand_description = self.request.data.get('brand_description',"")
            brand_logo = self.request.data.get('brand_logo',"")

            print(brand_name,brand_established_year,is_own_brand,brand_country,brand_description,brand_logo)

            missing_fields = []
            if brand_name == "":
                missing_fields.append("Brand name")
            if brand_established_year == "":
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
        
class UpdateProductBrands(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,product_brand_pk,format=None):
        try:
            product_brand_pk = product_brand_pk
            brand_name = self.request.data.get('brand_name',"")
            brand_established_year = self.request.data.get('brand_established_year',"")
            is_own_brand = self.request.data.get('is_own_brand',False)
            brand_country = self.request.data.get('brand_country',"")
            brand_description = self.request.data.get('brand_description',"")
            brand_logo = self.request.data.get('brand_logo',"")

            missing_fields = []
            if brand_name=="":
                missing_fields.append("Product Brand name")
            if brand_established_year == "":
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

class DeleteProductBrands(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
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
        
#product flavour
class FetchProductFlavour(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):
        try:
            pk = request.query_params.get('pk',"")
            product_flavour_name = request.query_params.get('product_flavour_name',"")

            if pk!= "":
                product_flavours,message = ManageProducts.fetch_product_flavour(pk=pk)
                product_flavours_data = product_serializers.Product_Flavour_Serializer(product_flavours,many=False)
            elif product_flavour_name!= "":
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
        
class CreateProductFlavour(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):

        try:
            product_flavour_name = self.request.data.get('product_flavour_name',"")
            if product_flavour_name == "":
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

class UpdateProductFlavour(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,product_flavour_pk,format=None):
        try:
            product_flavour_pk=product_flavour_pk
            product_flavour_name = self.request.data.get('product_flavour_name',"")
            if product_flavour_name == "":
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
        
class DeleteProductFlavour(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
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
        
#product
class FetchProduct(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):
        try:

            product_pk = self.request.query_params.get('product_pk',"")
            product_name = self.request.query_params.get('product_name',"")
            product_brand_pk = self.request.query_params.get('product_brand_pk',"")
            product_category_pk_list = self.request.query_params.get('product_category_pk_list',[])
            product_sub_category_pk_list = self.request.query_params.get('product_sub_category_pk_list',[])

            if product_pk!= "":
                product,message = ManageProducts.fetch_product(product_pk=product_pk)
                product_data = product_serializers.Product_Serializer(product,many=False)
            elif product_name!= "":
                product,message = ManageProducts.fetch_product(product_name=product_name)
                product_data = product_serializers.Product_Serializer(product,many=False)
            elif product_brand_pk!= "":
                product,message = ManageProducts.fetch_product(product_brand_pk=product_brand_pk)
                product_data = product_serializers.Product_Serializer(product,many=True)
            elif len(product_category_pk_list)!=0:
                product,message = ManageProducts.fetch_product(product_category_pk_list=product_category_pk_list)
                product_data = product_serializers.Product_Serializer(product,many=True)
            elif len(product_sub_category_pk_list)!= 0:
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

class FetchProductWithSKUAndDiscounts(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):
        try:

            product_pk = self.request.query_params.get('product_pk',"")
            product_brand_pk = self.request.query_params.get('product_brand_pk',"")
            product_category_pk = self.request.query_params.get('product_category_pk',"")
            product_sub_category_pk = self.request.query_params.get('product_sub_category_pk',"")

            if product_pk!= "":
                product,message = ManageProducts.fetch_product_with_sku_and_discount(product_pk=product_pk)
                product_data = product_serializers.Product_Serializer(product['product'],many=False).data
                product_data['product_sku'] = product_serializers.Product_SKU_Serializer(product['product_skus'],many=True).data
                product_data['product_discount'] = product_serializers.Product_Discount_Serializer(product['product_discount'],many=False).data
                product_data['product_images'] = product_serializers.Product_Images_Serializer(product['product_images'],many=True).data
            elif product_brand_pk!= "":
                product,message = ManageProducts.fetch_product_with_sku_and_discount(product_brand_pk=product_brand_pk)
                product_data = product_serializers.Product_Serializer(product['product'],many=True).data
                product_data['product_sku'] = product_serializers.Product_SKU_Serializer(product['product_skus'],many=True).data
                product_data['product_discount'] = product_serializers.Product_Discount_Serializer(product['product_discount'],many=True).data
                product_data['product_images'] = product_serializers.Product_Images_Serializer(product['product_images'],many=True).data
            elif product_category_pk!= "":
                product,message = ManageProducts.fetch_product_with_sku_and_discount(product_category_pk=product_category_pk)
                product_data = product_serializers.Product_Serializer(product['product'],many=True).data
                product_data['product_sku'] = product_serializers.Product_SKU_Serializer(product['product_skus'],many=True).data
                product_data['product_discount'] = product_serializers.Product_Discount_Serializer(product['product_discount'],many=True).data
                product_data['product_images'] = product_serializers.Product_Images_Serializer(product['product_images'],many=True).data
            elif product_sub_category_pk!= "":
                product,message = ManageProducts.fetch_product_with_sku_and_discount(product_sub_category_pk=product_sub_category_pk)
                product_data = product_serializers.Product_Serializer(product['product'],many=True).data
                product_data['product_sku'] = product_serializers.Product_SKU_Serializer(product['product_skus'],many=True).data
                product_data['product_discount'] = product_serializers.Product_Discount_Serializer(product['product_discount'],many=True).data
                product_data['product_images'] = product_serializers.Product_Images_Serializer(product['product_images'],many=True).data
            
            if product:
                return Response({
                    'message':message,
                    'product_data':product_data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message,
                },status=status.HTTP_400_BAD_REQUEST)
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
class CreateProduct(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):
        try:

            product_name = self.request.data.get('product_name',"")
            product_category_pk_list = self.request.data.get('product_category_pk_list',[])
            product_sub_category_pk_list = self.request.data.get('product_sub_category_pk_list',[])
            product_description = self.request.data.get('product_description',"")
            product_summary = self.request.data.get('product_summary',"")
            

            #can none
            product_brand_pk = self.request.data.get('product_brand_pk',"")
            product_ingredients = self.request.data.get('product_ingredients',"")
            product_usage_direction = self.request.data.get('product_usage_direction',"")

            missing_fields = []
            if product_name == "":
                missing_fields.append("Product Name")
            if len(product_category_pk_list) == 0:
                missing_fields.append("Product Categories")
            if len(product_sub_category_pk_list) == 0:
                missing_fields.append("Product Sub Categories")
            if product_description == "":
                missing_fields.append("Product Description")
            if product_summary=="":
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
        
class UpdateProduct(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,product_pk,format=None):
    
        try:
            product_pk = product_pk
            product_name = self.request.data.get('product_name',"")
            product_category_pk_list = self.request.data.get('product_category_pk_list',[])
            product_sub_category_pk_list = self.request.data.get('product_sub_category_pk_list',[])
            product_description = self.request.data.get('product_description',"")
            product_summary = self.request.data.get('product_summary',"")

            #can none
            product_brand_pk = self.request.data.get('product_brand_pk',"")
            product_ingredients = self.request.data.get('product_ingredients',"")
            product_usage_direction = self.request.data.get('product_usage_direction',"")

            missing_fields = []
            if product_name == "":
                missing_fields.append("Product Name")
            if len(product_category_pk_list) == 0:
                missing_fields.append("Product Categories")
            if len(product_sub_category_pk_list) == 0:
                missing_fields.append("Product Sub Categories")
            if product_description == "":
                missing_fields.append("Product Description")
            if product_summary == "":
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
        
class DeleteProduct(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
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

#product sku
class FetchProductSKU(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):
        try:

            pk = self.request.query_params.get('pk',"")
            product_id = self.request.query_params.get('product_id',"")
            product_name = self.request.query_params.get('product_name',"")
            product_sku = self.request.query_params.get('product_sku',"")

            if pk!= "":
                product_sku_fetch,message = ManageProducts.fetch_product_sku(pk=pk)
                product_sku_fetch_data = product_serializers.Product_SKU_Serializer(product_sku_fetch,many=False)
            elif product_id!= "":
                product_sku_fetch,message = ManageProducts.fetch_product_sku(product_id=product_id)
                product_sku_fetch_data = product_serializers.Product_SKU_Serializer(product_sku_fetch,many=True)
            elif product_name!= "":
                product_sku_fetch,message = ManageProducts.fetch_product_sku(product_name=product_name)
                product_sku_fetch_data = product_serializers.Product_SKU_Serializer(product_sku_fetch,many=False)
            elif product_sku!= "":
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

class CreateProductSKU(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):

        try:
            product_pk = self.request.data.get('product_pk',"")
            product_price = self.request.data.get('product_price',"")
            product_stock = self.request.data.get('product_stock',"")
            product_flavours_pk_list = self.request.data.get('product_flavours_pk_list',[])

            #can none
            product_color = self.request.data.get('product_color',"")
            product_size = self.request.data.get('product_size',"")

            missing_fields = []
            if product_pk == "":
                missing_fields.append("Product")
            if product_price=="":
                missing_fields.append("Price")
            if product_stock == "":
                missing_fields.append("Product stock")
            if len(product_flavours_pk_list)==0:
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
        
class UpdateProductSKU(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,product_sku_pk,format=None):
        try:

            product_sku_pk=product_sku_pk
            product_id = self.request.data.get('product_id',"")
            product_price = self.request.data.get('product_price',"")
            product_stock = self.request.data.get('product_stock',"")
            product_flavours_pk_list = self.request.data.get('product_flavours_pk_list',[])

            #can none
            product_color = self.request.data.get('product_color',"")
            product_size = self.request.data.get('product_size',"")

            missing_fields = []
            if product_id=="":
                missing_fields.append("Product")
            if product_price == "":
                missing_fields.append("Price")
            if product_stock == "":
                missing_fields.append("Product stock")
            if len(product_flavours_pk_list)==0:
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
        
class DeleteProductSKU(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
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
        
#product image
class FetchProductImages(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):
        try:
            product_pk = self.request.query_params.get('product_pk',"")
            product_image_pk = self.request.query_params.get('product_image_pk',"")
            if product_pk!= "":
                product_images,message = ManageProducts.fetch_product_image(product_pk=product_pk)
                product_images_data = product_serializers.Product_Images_Serializer(product_images,many=True,context={'request': request})
            elif product_image_pk!= "":
                product_images,message = ManageProducts.fetch_product_image(product_image_pk=product_image_pk)
                product_images_data = product_serializers.Product_Images_Serializer(product_images,many=False,context={'request': request})
            else:
                product_images,message = ManageProducts.fetch_product_image()
                product_images_data = product_serializers.Product_Images_Serializer(product_images,many=True,context={'request': request})
            
            if product_images:
                return Response({
                    'message':message,
                    'product_image_data':product_images_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
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
        
class CreateProductImages(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,product_id,format=None):
        try:
            product_id=product_id
            product_image_list = self.request.data.getlist('product_image_list',[])#as multiform data need to use getlist
            #can none
            color = self.request.data.get('color',"")
            size = self.request.data.get('size',"")


            if len(product_image_list)==0:
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
        
class UpdateProductImage(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,product_image_pk,format=None):
        try:
            product_image_pk=product_image_pk

            #can none
            new_image = self.request.data.get('new_image',"")
            color = self.request.data.get('color',"")
            size = self.request.data.get('size',"")

            product_image_updated,message = ManageProducts.update_product_image(request,product_image_pk,new_image,color,size)
            if product_image_updated:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

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
        
class DeleteProductImage(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
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

#product discount        
class FetchProductDiscount(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None,*args, **kwargs):
        try:
            
            product_id = self.request.query_params.get('product_id',"")
            discount_name = self.request.query_params.get('discount_name',"")
            is_active = self.request.query_params.get('is_active',False)
            product_discount_pk = self.request.query_params.get('product_discount_pk',"")
            brand_id = self.request.query_params.get('brand_id',"")
            sub_category_pk = self.request.query_params.get('sub_category_pk',"")
            category_pk = self.request.query_params.get('category_pk',"")
            product_id_pk= self.request.query_params.get('product_id_pk',"")
            brand_id_pk = self.request.query_params.get('brand_id_pk',"")
            sub_category_id_pk = self.request.query_params.get('sub_category_id_pk',"")
            category_id_pk = self.request.query_params.get('category_id_pk',"")
            product_id_pk_all = self.request.data.get('product_id_pk_all',False)
            brand_id_pk_all = self.request.data.get('brand_id_pk_all',False)
            sub_category_id_pk_all = self.request.data.get('sub_category_id_pk_all',False)
            category_id_pk_all = self.request.data.get('category_id_pk_all',False)

            if product_id!= "":
                product_discount,message = ManageProducts.fetch_product_discount(product_id=product_id)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif discount_name!= "":
                product_discount,message = ManageProducts.fetch_product_discount(discount_name=discount_name)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=False)
            elif is_active != False:
                product_discount,message = ManageProducts.fetch_product_discount(is_active=True)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif product_discount_pk!= "":
                product_discount,message = ManageProducts.fetch_product_discount(product_discount_pk=product_discount_pk)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=False)
            elif brand_id!= "":
                product_discount,message = ManageProducts.fetch_product_discount(brand_id=brand_id)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif sub_category_pk!= "":
                product_discount,message = ManageProducts.fetch_product_discount(sub_category_pk=sub_category_pk)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif category_pk!= "":
                product_discount,message = ManageProducts.fetch_product_discount(category_pk=category_pk)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif product_id_pk!= "":
                product_discount,message = ManageProducts.fetch_product_discount(product_id_pk=product_id_pk)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=False)
            elif brand_id_pk!= "":
                product_discount,message = ManageProducts.fetch_product_discount(brand_id_pk=brand_id_pk)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=False)
            elif sub_category_id_pk!= "":
                product_discount,message = ManageProducts.fetch_product_discount(sub_category_id_pk=sub_category_id_pk)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=False)
            elif category_id_pk!= "":
                product_discount,message = ManageProducts.fetch_product_discount(category_id_pk=category_id_pk)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=False)
            elif product_id_pk_all:
                product_discount,message = ManageProducts.fetch_product_discount(product_id_pk=True)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif brand_id_pk_all:
                product_discount,message = ManageProducts.fetch_product_discount(brand_id_pk=True)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif sub_category_id_pk_all:
                product_discount,message = ManageProducts.fetch_product_discount(sub_category_id_pk=True)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
            elif category_id_pk_all:
                product_discount,message = ManageProducts.fetch_product_discount(category_id_pk=True)
                product_discount_data = product_serializers.Product_Discount_Serializer(product_discount,many=True)
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
        
class CreateProductDiscount(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None,*args, **kwargs):

        try:
            discount_name = self.request.data.get('discount_name',"")
            discount_amount = self.request.data.get('discount_amount',"")
            start_date = self.request.data.get('start_date',"")
            end_date = self.request.data.get('end_date',"")
            # is_active = self.request.data.get('is_active',False)

            #any one from here
            product_id = self.request.data.get('product_id',"")
            brand_id = self.request.data.get('brand_id',"")
            sub_category_id = self.request.data.get('sub_category_id',"")
            category_id = self.request.data.get('category_id',"")

            missing_fields = []
            if discount_name == "":
                missing_fields.append("Discount Name")
            if discount_amount == "":
                missing_fields.append("Discount Amount")
            if start_date == "":
                missing_fields.append("Start date")
            if end_date == "":
                missing_fields.append("End date")

            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%f")
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%f")


            if missing_fields:
                return Response({
                    'error':f"The following fields are required: {', '.join(missing_fields)}"
                },status=status.HTTP_400_BAD_REQUEST)

            if start_date>end_date:
                return Response({
                    'error':"Start date of discount must be less than or equal to end data"
                },status=status.HTTP_400_BAD_REQUEST)
            
            if brand_id!="" and sub_category_id=="" and product_id=="" and category_id=="":
                discount_created,message = ManageProducts.create_product_discount(request,discount_name,discount_amount,start_date,end_date,"",brand_id,"","")
            elif sub_category_id!="" and brand_id=="" and product_id=="" and category_id=="":
                discount_created,message = ManageProducts.create_product_discount(request,discount_name,discount_amount,start_date,end_date,"","",sub_category_id,"")
            elif product_id!="" and brand_id=="" and sub_category_id=="" and category_id=="":
                discount_created,message = ManageProducts.create_product_discount(request,discount_name,discount_amount,start_date,end_date,product_id,"","","")
            elif category_id!="" and brand_id=="" and product_id=="" and sub_category_id=="":
                discount_created,message = ManageProducts.create_product_discount(request,discount_name,discount_amount,start_date,end_date,"","","",category_id)
            else:
                return Response({
                    'error':"Must provide either one of product id or brand id or sub category id or category id, not more than one"
                },status=status.HTTP_400_BAD_REQUEST)

            if discount_created:
                return Response({
                    'message':message
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

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
        
class UpdateProductDiscount(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,format=None):

        try:
            #getting the product discount
            product_discount_brand_id_pk = self.request.data.get('product_discount_brand_id_pk',"")
            product_discount_sub_category_id_pk = self.request.data.get('product_discount_sub_category_id_pk',"")
            product_discount_category_id_pk = self.request.data.get('product_discount_category_id_pk',"")
            product_discount_product_id_pk = self.request.data.get('product_discount_product_id_pk',"")

            
            discount_name = self.request.data.get('discount_name',"")
            discount_amount = self.request.data.get('discount_amount',"")
            start_date = self.request.data.get('start_date',"")
            end_date = self.request.data.get('end_date',"")
            # is_active = self.request.data.get('is_active',"")
            delete = self.request.data.get('delete',False)

            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%f")
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%f")

            #getting optional parametes, MUST have one
            brand_id = self.request.data.get('brand_id',"")
            sub_category_id = self.request.data.get('sub_category_id',"")
            category_id = self.request.data.get('category_id',"")
            product_id = self.request.data.get('product_id',"")

            missing_fields = []
            if product_id == "":
                missing_fields.append("Product")
            if discount_name == "":
                missing_fields.append("Discount name")
            if discount_amount == "":
                missing_fields.append("Discount amount")
            if start_date == "":
                missing_fields.append("Start date")
            if end_date == "":
                missing_fields.appned("End date")

            if missing_fields:
                return Response({
                    'error':f"The following fields are required: {', '.join(missing_fields)}"
                },status=status.HTTP_400_BAD_REQUEST)

            if start_date>end_date:
                return Response({
                    'error':"Start date of discount must be less than or equal to end data"
                },status=status.HTTP_400_BAD_REQUEST)
            
            if product_discount_brand_id_pk!="" and product_discount_sub_category_id_pk=="" and product_discount_category_id_pk=="" and product_discount_product_id_pk=="":
                updated,message = ManageProducts.update_product_discount_for_brand(request,product_discount_brand_id_pk,discount_name,discount_amount,start_date,end_date,brand_id,False,delete)
            elif product_discount_sub_category_id_pk!="" and product_discount_brand_id_pk=="" and product_discount_category_id_pk=="" and product_discount_product_id_pk == "":
                updated,message = ManageProducts.update_product_discount_for_sub_category(request,product_discount_sub_category_id_pk,discount_name,discount_amount,start_date,end_date,sub_category_id,False,delete)
            elif product_discount_category_id_pk!="" and product_discount_brand_id_pk=="" and product_discount_sub_category_id_pk=="" and product_discount_product_id_pk=="":
                updated,message = ManageProducts.update_product_discount_for_category(request,product_discount_category_id_pk,discount_name,discount_amount,start_date,end_date,category_id,False,delete)
            elif product_discount_product_id_pk!="" and  product_discount_brand_id_pk=="" and product_discount_sub_category_id_pk=="" and product_discount_category_id_pk=="":
                updated, message = ManageProducts.update_product_discount_for_product(request,product_discount_product_id_pk,discount_name,discount_amount,start_date,end_date,product_id,False,delete)
           
            if updated:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

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
        
#position for admin
class FetchPositionForAdmin(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):

        try:

            admin_user_name = self.request.data.get('admin_user_name',"")
            if admin_user_name == "":
                return Response({
                    'error':"User name needed for fetching position"
                },status=status.HTTP_400_BAD_REQUEST)


            fetch_admin_position,message = AdminManagement.fetch_postion_of_admin(request,admin_user_name)
            fetch_admin_position_data = serializers.AdminPositionSerializer(fetch_admin_position,many=False)
            if fetch_admin_position:
                return Response({
                    'message':message,
                    'position':fetch_admin_position_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

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

class AddPositionForAdmin(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):
        try:
            admin_user_name = self.request.data.get('admin_user_name',"")
            if admin_user_name == "":
                return Response({
                    'error':"User name needed for position"
                },status=status.HTTP_400_BAD_REQUEST)
            
            position_pk = self.request.data.get('position_pk',"")
            if position_pk == "":
                return Response({
                    'error':"Postion needed"
                },status=status.HTTP_400_BAD_REQUEST)
            
            added,message = AdminManagement.add_user_admin_position(request,admin_user_name,position_pk)
            if added:
                return Response({
                    'message':message,
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

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
        
class UpdatePositionForAdmin(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,format=None):
        try:
            admin_user_name = self.request.data.get('admin_user_name',"")
            if admin_user_name == "":
                return Response({
                    'error':"User name needed for position"
                },status=status.HTTP_400_BAD_REQUEST)
            
            position_pk = self.request.data.get('position_pk',"")

            
            updated,message = AdminManagement.update_user_admin_position(request,admin_user_name,position_pk)
            if updated:
                return Response({
                    'message':message,
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)

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

class RemovePositionForAdmin(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
    def delete(self,request,format=None):
        try:
            admin_user_name = self.request.data.get('admin_user_name',"")
            delete = self.request.data.get('delete',False)
            if admin_user_name == "":
                return Response({
                    'error':"User name needed for position"
                },status=status.HTTP_400_BAD_REQUEST)
            
            deleted,message = AdminManagement.remove_position_of_admin(request,admin_user_name,delete)
            if deleted:
                return Response({
                    'message':message
                },status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
            
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
        
#admin role permission
class FetchBusinessAdminRolePermission(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='GET', block=True))
    def get(self,request,format=None):
        try:

            admin_role_permission_pk = self.request.query_params.get('admin_role_permission_pk',"")
            admin_position_pk = self.request.query_params.get('admin_position_pk',"")
            admin_permission_pk = self.request.query_params.get('admin_permission_pk',"")

            if admin_role_permission_pk!= "":
                admin_role_permission,message = AdminManagement.fetch_admin_role_permission(admin_role_permission_pk=admin_role_permission_pk)
                admin_role_permission_data = serializers.AdminRolePermissionSerializer(admin_role_permission,many=False)
            elif admin_position_pk!= "":
                admin_role_permission,message = AdminManagement.fetch_admin_role_permission(admin_position_pk=admin_position_pk)
                admin_role_permission_data = serializers.AdminRolePermissionSerializer(admin_role_permission,many=True)
            elif admin_permission_pk!= "":
                admin_role_permission,message = AdminManagement.fetch_admin_role_permission(admin_permission_pk=admin_permission_pk)
                admin_role_permission_data = serializers.AdminRolePermissionSerializer(admin_role_permission,many=True)
            else:
                admin_role_permission,message = AdminManagement.fetch_admin_role_permission()
                admin_role_permission_data = serializers.AdminRolePermissionSerializer(admin_role_permission,many=True)
            
            if admin_role_permission:
                return Response({
                    'message':message,
                    'admin_role_permission':admin_role_permission_data.data
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
   

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

class CreateBusinessAdminRolePermission(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='POST', block=True))
    def post(self,request,format=None):

        try:
            admin_position_pk = self.request.data.get('admin_position_pk',"")
            admin_permission_pk_list = self.request.data.get('admin_permission_pk_list',[])
            if admin_position_pk == "":
                return Response({
                    'error':"Admin position is needed"
                },status=status.HTTP_400_BAD_REQUEST)
            if len(admin_permission_pk_list)==0:
                return Response({
                    'error':"Atleast 1 permission is needed"
                },status=status.HTTP_400_BAD_REQUEST)
            
            created,message = AdminManagement.create_admin_role_permission(request,admin_position_pk,admin_permission_pk_list)
            if created:
                return Response({
                    'message':message
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
            
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
        
class UpdateBusinessAdminRolePermission(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='PUT', block=True))
    def put(self,request,admin_position_pk,format=None):
        try:

            admin_position_pk = admin_position_pk
            admin_permission_pk_list = self.request.data.get('admin_permission_pk_list',[])
            
            updated,message = AdminManagement.update_admin_role_permission(request,admin_position_pk,admin_permission_pk_list)
            if updated:
                return Response({
                    'message':message
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
            
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
        
class DeleteBusinessAdminRolePermission(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate=REFRESH_RATE, method='DELETE', block=True))
    def delete(self,request,admin_position_pk,format=None):
        try:
            
            admin_position_pk = admin_position_pk
            deleted,message = AdminManagement.delete_admin_role_permission(request,admin_position_pk)
            if deleted:
                return Response({
                    'message':message
                },status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({
                    'error':message
                },status=status.HTTP_400_BAD_REQUEST)
            
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