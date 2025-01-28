from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django_resized import ResizedImageField

# Create your models here.

class AccountsManager(BaseUserManager):
    
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user



def get_customer_avatar_path(self, filename):
    return f'customer_profile_picture/{self.pk}/{filename}'
class Accounts(AbstractBaseUser):
    '''This model is for storing customer data'''

    SKIN_TYPE_CHOICES=[
        ('normal','Normal'),
        ('oily','Oily'),
        ('dry','Dry'),
        ('combination','Combination'),
        ('sensitive','Sensitive'),
    ]

    email=models.EmailField(max_length=254,unique=True,verbose_name="Email Address",null=False,blank=False) #Used for login accounts
    username = models.CharField(max_length=50,verbose_name="Username",null=False,blank=False)
    
    first_name=models.CharField(max_length=50,verbose_name="Full name")
    middle_name=models.CharField(max_length=50,verbose_name="Middle name")
    last_name=models.CharField(max_length=50,verbose_name="Last name")
    phone_no=models.CharField(max_length=15,verbose_name="Phone Number") 
    profile_picture = ResizedImageField(size=[244,244],upload_to=get_customer_avatar_path,blank=True, null=True)
    skinType=models.CharField(max_length=20,choices=SKIN_TYPE_CHOICES,blank=True,verbose_name="Skin Type")
    block=models.BooleanField(default=False,verbose_name="Block Account")

    date_joined=models.DateTimeField(auto_now_add=True,verbose_name="Date Joined",null=False,blank=False)
    last_login=models.DateTimeField(auto_now=True,verbose_name="Last Login")
    
    is_active=models.BooleanField(default=True,verbose_name="Active")
    
    is_admin=models.BooleanField(default=False,verbose_name="Admin")
    is_staff=models.BooleanField(default=False,verbose_name="Staff")
    is_superuser=models.BooleanField(default=False,verbose_name="Superuser")
    
    objects=AccountsManager()
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True



class ErrorLogs(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True,null=True)  # Automatically logs the time of the error
    error_type = models.CharField(max_length=255,null=True,blank=True)  # The type of error, e.g., "DatabaseError"
    error_message = models.TextField(null=True,blank=True)  # The detailed error message

    class Meta:
        verbose_name = "Error Log"
        verbose_name_plural = "Error Logs"
        ordering = ['-timestamp']  # Orders the errors by latest timestamp first

    def __str__(self):
        return f"{self.timestamp} - {self.error_type}"