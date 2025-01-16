from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone

# Create your models here.


def get_customer_avatar(instance, filename):
    return f'customer_profile_picture/{instance.customer_id}/{filename}'
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
    unique_id=models.CharField(max_length=50,unique=True,verbose_name="Unique ID")
    profile_picture = models.ImageField(upload_to=get_customer_avatar, null=True, blank=True,verbose_name="Profile Picture")
    username = models.CharField(max_length=50,unique=True,verbose_name="Username")
    skinType=models.CharField(max_length=20,choices=SKIN_TYPE_CHOICES,blank=True,verbose_name="Skin Type")
    email=models.EmailField(max_length=254,unique=True,verbose_name="Email Address")
    address=models.TextField(verbose_name="Address")
    phone=models.CharField(max_length=15,verbose_name="Phone") 
    block=models.BooleanField(default=False,verbose_name="Block Customer")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Created At")
    updated_at=models.DateTimeField(auto_now=True,verbose_name="Updated At")

    def __str__(self):
        return f"{self.unique_id} - {self.full_name}"
    
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
    customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="Coupons",verbose_name="Customer ID")
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