from django.db import models
from customer.models import Customer
from products.models import Product_SKU
from business_admin.models import BusinessAdminUser
# Create your models here.

class Order(models.Model):
    
    ORDER_STATUS_CHOICES=[
        ('pending','Pending'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled'),
        ('returned','Returned'),
        ('refunded','Refunded'),
    ]
    
    order_id=models.CharField(null=False,blank=False,max_length=100,unique=True) # Each order will have a unique order_id that will be genetated by the system
    customer_id = models.ForeignKey(Customer, null=False,blank=False,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(null=False,blank=False,max_digits=10,decimal_places=2)
    order_status = models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES,default='pending',null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(BusinessAdminUser,null=True,blank=True,on_delete=models.CASCADE,related_name="OrderUpdatedBy")

    class Meta:
        verbose_name="Order"
        verbose_name_plural="Orders"
    
    def __str__(self):
        return self.order_id

class OrderDetails(models.Model):
    '''Stores all the details of the order related to the product'''
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE,null=False,blank=False)
    product_sku=models.ForeignKey(Product_SKU,on_delete=models.CASCADE,null=False,blank=False)
    quantity=models.PositiveIntegerField(null=False,blank=False)
    units=models.PositiveIntegerField(null=False,blank=False,default=1)
    subtotal=models.DecimalField(null=False,blank=False,max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True,null=False,blank=False)
    updated_at=models.DateTimeField(auto_now=True,null=False,blank=False)
    
    class Meta:
        verbose_name="Order Detail"
        verbose_name_plural="Order Details"
    
    def __str__(self):
        return str(self.pk)
    
class OrderShippingAddress(models.Model):
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE,null=False,blank=False)
    address_line1=models.CharField(null=True,blank=True,max_length=200)
    address_line2=models.CharField(null=True,blank=True,max_length=200)
    country=models.CharField(null=True,blank=True,max_length=100)
    city=models.CharField(null=True,blank=True,max_length=100)
    postal_code=models.CharField(null=True,blank=True,max_length=50)    
    class Meta:
        verbose_name="Order Shipping Address"
        verbose_name_plural="Order Shipping Addresses"
    
    def __str__(self):
        return str(self.pk)

class OrderPayment(models.Model):
    '''Stores all the payment details of the order'''
    
    PAYMENT_MODE_CHOICES=[
        ('credit_card','Credit Card'),
        ('debit_card','Debit Card'),
        ('net_banking','Net Banking'),
        ('wallet','Wallet'),
        ('bkash','bKash'),
        ('rocket','Rocket'),
        ('nagad','Nagad'),
        ('cash_on_delivery','Cash On Delivery')
    ]
    
    PAYMENT_STATUS=[
        ('pending','Pending'),
        ('success','Success'),
        ('failed','Failed')
    ]
    
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE,null=False,blank=False)
    payment_mode=models.CharField(null=False,blank=False,max_length=50,choices=PAYMENT_MODE_CHOICES)
    payment_status=models.CharField(null=False,blank=False,max_length=50,choices=PAYMENT_STATUS,default='pending')
    payment_date=models.DateTimeField(auto_now_add=True,null=False,blank=False)
    payment_amount=models.DecimalField(null=False,blank=False,max_digits=10,decimal_places=2)
    payment_reference=models.CharField(null=False,blank=False,max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=False,blank=False)
    updated_at=models.DateTimeField(auto_now=True,null=False,blank=False)
    
    class Meta:
        verbose_name="Order Payment"
        verbose_name_plural="Order Payments"
    
    def __str__(self):
        return str(self.pk)

class Cart(models.Model):
    '''This model is for storing customer cart data'''
    
    device_ip=models.GenericIPAddressField(verbose_name="Device IP") #Storing device IP So that if the customer is not logged in, we can still track the cart
    customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="Cart") #Store customer id if the user is logged in
    cart_total_amount=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Cart Total Amount")
    cart_checkout_status=models.BooleanField(default=False,verbose_name="Cart Checkout Status")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Created At")
    updated_at=models.DateTimeField(auto_now=True,verbose_name="Updated At")
    
    class Meta:
        verbose_name="Customer Cart"
        verbose_name_plural="Customer Carts"
    
    def __str__(self):
        return str(self.pk)

class CartItems(models.Model):
    cart_id=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product_sku=models.ForeignKey(Product_SKU,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1,verbose_name="Quantity")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Created At")
    updated_at=models.DateTimeField(auto_now=True,verbose_name="Updated At")

    def __str__(self):
        return str(self.pk)
