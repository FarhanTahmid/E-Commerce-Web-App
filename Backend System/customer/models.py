from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Customer(models.Model):
    '''This model is for storing customer data'''

    SKIN_TYPE_CHOICES=[
        ('normal','Normal'),
        ('oily','Oily'),
        ('dry','Dry'),
        ('combination','Combination'),
        ('sensitive','Sensitive'),
    ]

    full_name=models.CharField(max_length=100,verbose_name="Full name")
    email=models.EmailField(max_length=254,unique=True,verbose_name="Email Address")
    address=models.TextField(verbose_name="Address")
    phone=models.CharField(max_length=15,verbose_name="Phone") 
    skinType=models.CharField(max_length=20,choices=SKIN_TYPE_CHOICES,blank=True,verbose_name="Skin Type")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Created At")
    updated_at=models.DateTimeField(auto_now=True,verbose_name="Updated At")

class Coupon(models.Model):
    '''This model is for discount coupon for customer'''

    coupon_code=models.CharField(max_length=50,unique=True,verbose_name="Coupon Code")
    discount_percentage=models.PositiveIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(100)],
        verbose_name="Discount Percentage")
    
    maximum_discount_amount=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Maximum Discount Amount")
    start_date=models.DateTimeField(verbose_name="Start Date")
    end_date=models.DateTimeField(verbose_name="End Date")
    is_active=models.BooleanField(default=True,verbose_name="Is Active")
    usage_limit=models.PositiveIntegerField(default=1,verbose_name="Usage Limit")
    customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="Coupons",verbose_name="Customer ID")

    def __str__(self):
        return self.coupon_code