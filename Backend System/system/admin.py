from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(ErrorLogs)
class ErrorLog(admin.ModelAdmin):
    list_display=[
        'id','timestamp','error_type'
    ]