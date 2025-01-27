from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(CustomCustomerManager)
class CustomCustomerManagerAdmin(admin.ModelAdmin):
    list_display=[
        'email'
    ]