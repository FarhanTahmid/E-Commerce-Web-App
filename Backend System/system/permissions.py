from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from django.urls import get_resolver,URLResolver, URLPattern
from business_admin.admin_management import AdminManagement
from business_admin.models import AdminRolePermission
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


                api_views[view_class_name] = list(permissions)

    return api_views

class HasPermission(BasePermission):
    """
    Custom permission to check if the user has ANY of the required permissions.
    """

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True
        
        if request.user.is_admin:
            try:
                #Get the user's role

                #admin user role instance
                user_role = request.user.admin_role.role #Manager/Owner/Staff
                if not user_role:
                    return False

                #Check if the role has ANY of the required permissions
                api_permission_mapping = extract_views_from_urlpatterns(get_resolver().url_patterns)
                required_permission_name = api_permission_mapping.get(view.__class__.__name__, None)
                if not required_permission_name:
                    return False
                
                required_permission_name=required_permission_name[0]
                admin_role_permissions = AdminRolePermission.objects.filter(role=user_role)
                for p in admin_role_permissions:
                    if p.permission.permission_name.lower() in required_permission_name:
                        return True

                admin_user_role = request.user.admin_role.extra_permissions.all()
                if admin_user_role:

                    for p in admin_user_role:
                        if p.permission_name == required_permission_name:
                            return True
                
                return False

            except ObjectDoesNotExist:
                return False
        else:
            return False

def create_permissions(sender, **kwargs):
    from business_admin.models import AdminPermissions
    """Create permissions based on extracted API views."""
    from django.db.utils import OperationalError, ProgrammingError

    try:
        api_permission_mapping = extract_views_from_urlpatterns(get_resolver().url_patterns)

        for permissions in api_permission_mapping.values():
            for permission_name in permissions:
                obj, created = AdminPermissions.objects.get_or_create(permission_name=permission_name)
        
        AdminPermissions.objects.get_or_create(permission_name='view')
        AdminPermissions.objects.get_or_create(permission_name='create')
        AdminPermissions.objects.get_or_create(permission_name='update')
        AdminPermissions.objects.get_or_create(permission_name='delete')

    except (OperationalError, ProgrammingError):
        print("Skipping permission creation (DB not ready).")