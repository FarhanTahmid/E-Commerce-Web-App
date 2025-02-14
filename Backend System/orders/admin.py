from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('device_ip', 'customer_id', 'cart_total_amount','created_at','cart_checkout_status')
    
@admin.register(CartItems)
class CartItemLists(admin.ModelAdmin):
    list_display = ('cart_id','product_sku','quantity','created_at')