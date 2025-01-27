from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django_resized import ResizedImageField

class CustomerUser(AbstractBaseUser):
    """
    Custom user model for managing customer accounts in the e-commerce application.

    This model extends Django's built-in `AbstractUser` to customize user authentication 
    based on email rather than the traditional username. The `email` field is unique 
    and serves as the primary identifier for login. Additional attributes and functionality 
    can be added to meet the specific requirements of customer management.

    Attributes:
        email (EmailField):
            - The unique email address for each customer user.
            - Acts as the primary identifier for authentication and login.
            - Must be unique across all users.

        is_active (BooleanField):
            - Indicates whether the user account is currently active.
            - Default value is `True`.
            - Inactive accounts are typically used for deactivating users without deleting them.

    Methods:
        __str__():
            - Returns a string representation of the user, which is the `email` address.
            - Useful for debugging and when working with user objects in templates and the admin panel.

    Meta:
        verbose_name (str):
            - A human-readable singular name for the model.
            - Default: `'Customer User'`.

        verbose_name_plural (str):
            - A human-readable plural name for the model.
            - Default: `'Customer Users'`.

    Example Usage:
        # Creating a new CustomerUser
        user = CustomerUser.objects.create_user(
            email="customer@example.com",
            password="securepassword123"
        )

        # Checking if a user is active
        if user.is_active:
            print(f"{user.email} is an active customer.")

        # Displaying the user as a string
        print(user)  # Output: customer@example.com
    """
    email = models.EmailField(
        max_length=255,
        unique=True,
        help_text="The user's unique email address."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the user account is active."
    )
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=('username',)
    
    def __str__(self):
        """
        Returns the string representation of the user, which is the email address.

        This method is particularly useful in the Django admin, debugging sessions, 
        and when working with user objects in templates.

        Returns:
            str: The user's email address.
        """
        return self.email

    class Meta:
        verbose_name = 'Customer User'
        verbose_name_plural = 'Customer Users'


def get_customer_avatar_path(instance, filename):
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
    unique_id=models.CharField(max_length=50,unique=True,verbose_name="Unique ID",primary_key=True)
    profile_picture = ResizedImageField(size=[244,244],upload_to=get_customer_avatar_path,blank=True, null=True)
    username = models.CharField(max_length=50,unique=True,verbose_name="Username")
    skinType=models.CharField(max_length=20,choices=SKIN_TYPE_CHOICES,blank=True,verbose_name="Skin Type")
    email=models.EmailField(max_length=254,unique=True,verbose_name="Email Address")
    phone_no=models.CharField(max_length=15,verbose_name="Phone") 
    block=models.BooleanField(default=False,verbose_name="Block Customer")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Created At")
    updated_at=models.DateTimeField(auto_now=True,verbose_name="Updated At")

    def __str__(self):
        return self.unique_id

class CustomerAddress(models.Model):
    customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
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