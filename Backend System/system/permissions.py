from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from business_admin.models import *
from django.urls import get_resolver,URLResolver, URLPattern
import re

ACTION_KEYWORDS = {
    "create": "create",
    "update": "update",
    "delete": "delete",
    "fetch": "view"
}
def extract_views_from_urlpatterns(urlpatterns, base_path=""):
    """Recursively extracts class-based API views from urlpatterns"""
    api_views = {}

    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            # Recursively fetch views from nested urlpatterns
            nested_api_views = extract_views_from_urlpatterns(pattern.url_patterns, base_path + pattern.pattern.regex.pattern)
            api_views.update(nested_api_views)
        elif isinstance(pattern, URLPattern):
            if hasattr(pattern.callback, 'view_class'):  # Ensure it's a class-based view
                view_class_name = pattern.callback.view_class.__name__
                # Extract main resource name
                resource_name = re.sub(r'^(Create|Update|Delete|Fetch)', '', view_class_name)
                resource_name = re.sub(r'View$', '', resource_name) 
                # Convert to snake_case
                resource_name_snake = re.sub(r'([A-Z])', r'_\1', resource_name).lower().strip('_')

                # Generate permissions dynamically
                permissions = set()
                for keyword, perm_action in ACTION_KEYWORDS.items():
                    if keyword.lower() in view_class_name.lower():
                        permissions.add(f"{perm_action}_{resource_name_snake}")

                # Always add "view" permission by default
                # permissions.add(f"view_{resource_name_snake}")

                api_views[view_class_name] = list(permissions)

    return api_views

class IsAdminWithPermission(BasePermission):
    """
    Custom permission to check if the user has ANY of the required permissions.
    """
    # def __init__(self, required_permissions=None):
    #     self.required_permissions = required_permissions or []

    def has_permission(self, request, view):

        # if request.user.is_superuser:
        #     return True
        
        # if request.user.is_admin:
        #     try:
                # Get the user's role

                # user_role = request.user.admin_role.role
                # if not user_role:
                #     return False

                # Check if the role has ANY of the required permissions
                # if self.required_permissions:
                #     return AdminRolePermission.objects.filter(
                #         role = user_role,
                #         permission__permission_name__in=self.required_permissions
                #     ).exists()

                api_permission_mapping = extract_views_from_urlpatterns(get_resolver().url_patterns)
                print(api_permission_mapping)
                required_permission_name = api_permission_mapping.get(view.__class__.__name__, None)
                if not required_permission_name:
                    return False
                permission, created = AdminPermissions.objects.get_or_create(permission_name=required_permission_name[0])
                if created:
                    print(f"New permission '{required_permission_name}' saved in AdminPermissions.")
                # has_permission = (
                #     AdminRolePermission.objects.filter(role=user_role, permission__permission_name=required_permission_name).exists()
                #     # or extra_permissions.filter(permission_name=required_permission_name).exists()
                # )

                return True

        #     except ObjectDoesNotExist:
        #         return False
        # else:
        #     return False