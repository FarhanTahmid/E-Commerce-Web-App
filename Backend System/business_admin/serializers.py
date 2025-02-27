from rest_framework import serializers
from .models import *

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

    class Meta:
        model = AdminUserRole
        fields = '__all__'
