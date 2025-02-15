from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(AdminPermissions)
class AdminPermissionsAdmin(admin.ModelAdmin):
    list_display = ('pk','permission_name','permission_description','created_at','updated_at')
    search_fields = ('permission_name','permission_description')
    list_filter = ('created_at','updated_at')