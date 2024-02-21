from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Business_Identity)
class Business_Identity(admin.ModelAdmin):
    list_display=[
        'business_name','platform_product_key'
    ]
@admin.register(Comapany_Users)
class Company_Users(admin.ModelAdmin):
    list_display=[
        'first_name','last_name','email','is_super_user','is_staff','is_employee'
    ]