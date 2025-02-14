from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields = ('email','username')
    readonly_fields = ('date_joined','last_login','id')
    filter_horizontal = ()
    list_filter = ('is_admin','is_staff','is_superuser')
    fieldsets = ()
    
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','username','password1','password2')
        }),
    )


admin.site.register(Accounts,AccountAdmin)

@admin.register(ErrorLogs)
class ErrorLog(admin.ModelAdmin):
    list_display=[
        'id','timestamp','error_type'
    ]