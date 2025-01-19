from rest_framework.permissions import BasePermission

class IsAdminOrSuperuser(BasePermission):
    """
    Custom permission to only allow superusers and admin users.
    """

    def has_permission(self, request, view):
        # Check if the user is a superuser or staff (admin)
        return request.user and (request.user.is_superuser or request.user.is_staff)

class IsBusinessOwner(BasePermission):
    """
    Custom permission to only allow Business Owner
    """
    def has_permission(self, request, view):
        pass

class IsModerator(BasePermission):
    """
    Custom permission to only allow Business Owner
    """
    def has_permission(self, request, view):
        pass

class IsManager(BasePermission):
    """
    Custom permission to only allow Business Owner
    """
    def has_permission(self, request, view):
        pass