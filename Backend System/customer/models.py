from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django_resized import ResizedImageField
from system.models import Accounts

class CustomerAddress(models.Model):
    customer_id=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    address_title=models.CharField(null=True,blank=True,max_length=100)
    address_line1=models.CharField(null=True,blank=True,max_length=200)
    address_line2=models.CharField(null=True,blank=True,max_length=200)
    country=models.CharField(null=True,blank=True,max_length=100)
    city=models.CharField(null=True,blank=True,max_length=100)
    postal_code=models.CharField(null=True,blank=True,max_length=50)
    created_at=models.DateTimeField(null=False,blank=False,auto_now_add=True)
    updated_at=models.DateTimeField(null=False,blank=False,auto_now_add=True)

    class Meta:
        verbose_name="Customer Address"
    
    def __str__(self):
        return self.customer_id

    
class Coupon(models.Model):
    '''This model is for discount coupon for customer'''

    DISCOUNT_TYPE_CHOICES=[
        ('percentage','Percentage'),
        ('fixed','fixed'),
        ('refund','Refund')
    ]

    coupon_code=models.CharField(max_length=50,unique=True,verbose_name="Coupon Code")
    discount_type = models.CharField(max_length=20,choices=DISCOUNT_TYPE_CHOICES,blank=True,verbose_name="Discount Type")
    discount_percentage=models.PositiveIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(100)],
        verbose_name="Discount Percentage")
    discount_amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Discount Amount")
    maximum_discount_amount=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Maximum Discount Amount")
    start_date=models.DateTimeField(verbose_name="Start Date")
    end_date=models.DateTimeField(verbose_name="End Date")
    usage_limit=models.PositiveIntegerField(default=1,verbose_name="Usage Limit")
    customer_id=models.ForeignKey(Accounts,on_delete=models.CASCADE,related_name="Coupons",verbose_name="Customer ID")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Created At")
    updated_at=models.DateTimeField(auto_now=True,verbose_name="Updated At")

    def __str__(self):
        return self.coupon_code
    
    def is_coupon_valid(self):
        '''Check if the coupon is valid'''
        now = timezone.now()
        if self.start_date <= now and now <= self.end_date:
            return True
        else:
            return False