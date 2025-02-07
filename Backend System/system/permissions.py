from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from business_admin.models import *

class IsAdminWithPermission(BasePermission):
    """
    Custom permission to check if the user has ANY of the required permissions.
    """
    def __init__(self, required_permissions=None):
        self.required_permissions = required_permissions or []

    def has_permission(self, request, view):

    
        if not request.user or not request.user.is_authenticated:
            return False  # User must be authenticated

        if request.user.is_superuser:
            return True
        
        if request.user.is_admin:
            try:
                # Get the user's role
                user_role = request.user.admin_role.role
                if not user_role:
                    return False
                # Check if the role has ANY of the required permissions
                if self.required_permissions:
                    return AdminRolePermission.objects.filter(
                        role = user_role,
                        permission__permission_name__in=self.required_permissions
                    ).exists()
                
                return False
            except ObjectDoesNotExist:
                return False
        else:
            return False