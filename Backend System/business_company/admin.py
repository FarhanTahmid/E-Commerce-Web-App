from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Business_Identity)
class Business_Identity(admin.ModelAdmin):
    list_display=[
        'business_name','platform_product_key'
    ]