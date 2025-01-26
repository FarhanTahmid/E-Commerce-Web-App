from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django_resized import ResizedImageField
# Create your models here.

# Models for custom customer user login and management
class CustomerManager(BaseUserManager):
    """
    Custom manager for the CustomerUser model.

    This manager provides methods for creating user instances with proper
    handling of email normalization and password hashing. It is intended
    to manage the lifecycle of `CustomerUser` objects.

    Methods:
        create_user(email, password=None):
            Creates and returns a new `CustomerUser` instance with the specified email
            and password.

    Example Usage:
        CustomerUser.objects.create_user(email='user@example.com', password='securepassword123')

    Raises:
        ValueError: If the email is not provided.
    """

    def create_user(self, email, password=None):
        """
        Creates and returns a new `CustomerUser` instance.

        Parameters:
            email (str): The email address for the new user. Must be unique.
            password (str, optional): The password for the new user. Defaults to None.

        Returns:
            CustomerUser: A new `CustomerUser` instance with the provided email and password.

        Example:
            user = CustomerUser.objects.create_user(
                email='user@example.com',
                password='securepassword123'
            )
        """
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)  # Normalize the email for consistency
        user = self.model(email=email)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)
        return user

class CustomerUser(AbstractBaseUser):
    """
    Custom user model for managing customers in the e-commerce application.

    This model uses email as the unique identifier for authentication instead
    of a traditional username. It is designed to handle the unique needs of
    customer accounts, such as email-based login and account activity status.

    Attributes:
        email (EmailField): The unique email address for the user.
        is_active (BooleanField): Indicates whether the user account is active. Defaults to True.

    Methods:
        __str__(): Returns a string representation of the user, which is the email.

    Meta:
        verbose_name (str): A human-readable singular name for the model.
        verbose_name_plural (str): A human-readable plural name for the model.
    """
    email = models.EmailField(max_length=255, unique=True, help_text="The user's unique email address.")
    is_active = models.BooleanField(default=True, help_text="Indicates whether the user account is active.")

    objects = CustomerManager()

    USERNAME_FIELD = 'email'  # Specifies that email is the unique identifier for authentication

    def __str__(self):
        """
        Returns the string representation of the user, which is the email address.

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