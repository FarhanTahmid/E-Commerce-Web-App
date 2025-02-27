from rest_framework import serializers
from .models import *
from system.serializer import *

class AdminPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPositions
        fields = '__all__'
class AdminPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPermissions
        fields= '__all__'
class AdminRolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRolePermission
        fields = '__all__'
class BusinessAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAdminUser
        fields = '__all__'

class AdminUserRoleSerializer(serializers.ModelSerializer):

    user = Account_Serialier(read_only=True)
    role = AdminPositionSerializer(read_only=True)
    
    class Meta:
        model = AdminUserRole
        fields = '__all__'
