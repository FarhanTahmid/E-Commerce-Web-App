from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Product_Category)
class Product_Category_Admin(admin.ModelAdmin):
    list_display=['category_name','description','created_at','updated_at']
    search_fields=['category_name','description']
    list_filter=['created_at','updated_at']

@admin.register(Product_Sub_Category)
class Product_Sub_Category_Admin(admin.ModelAdmin):
    list_display=['sub_category_name','description','created_at','updated_at']
    search_fields=['sub_category_name','description']
    list_filter=['created_at','updated_at']
