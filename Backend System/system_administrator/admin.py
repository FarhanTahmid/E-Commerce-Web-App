from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(SystemErrors)
class SystemErrors(admin.ModelAdmin):
    list_display=[
        'date_time','error_name','error_occured_for','error_traceback','error_fix_status'
    ]
