from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(AdminPermissions)
class AdminPermissionsAdmin(admin.ModelAdmin):
    list_display = ('pk','permission_name','permission_description','created_at','updated_at')
    search_fields = ('permission_name','permission_description')
    list_filter = ('created_at','updated_at')

@admin.register(AdminUserRole)
class AdminUserRoleAdmin(admin.ModelAdmin):
    list_display = ['user','role','updated_by']

@admin.register(AdminPositions)
class AdminPositionAdmin(admin.ModelAdmin):
    list_display = ['name','description']

@admin.register(BusinessAdminUser)
class BusinessAdminUserAdmin(admin.ModelAdmin):
    list_display = ['admin_full_name',
                    'admin_user_name',
                    'admin_position',
                    'admin_email',
                    'login_request',
                    ]