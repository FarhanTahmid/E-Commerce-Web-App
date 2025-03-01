from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django_resized import ResizedImageField

# Create your models here.

class AccountsManager(BaseUserManager):
    """
    Custom manager for the Accounts model, providing methods to create regular users and superusers.

    Methods:
        create_user(email, username, password=None):
            Creates and returns a new user instance with the provided email, username, and password.
            - Email and username are required.
            - Password is securely hashed using Django's set_password method.

        create_superuser(email, username, password=None):
            Creates and returns a new superuser instance with the provided email, username, and password.
            - Superuser privileges (is_admin, is_staff, is_superuser) are enabled by default.

    Raises:
        ValueError: If email or username is not provided.

    Example Usage:
        # Creating a regular user
        user = Accounts.objects.create_user(
            email="user@example.com",
            username="user123",
            password="securepassword123"
        )

        # Creating a superuser
        superuser = Accounts.objects.create_superuser(
            email="admin@example.com",
            username="admin123",
            password="adminpassword"
        )
    """

    def create_user(self, email, username, password=None):
        """
        Creates and returns a new user instance.

        Parameters:
            email (str): The unique email address for the user.
            username (str): The username for the user.
            password (str, optional): The password for the user. Defaults to None.

        Returns:
            Accounts: A new user instance with the hashed password.

        Raises:
            ValueError: If email or username is not provided.
        """
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and returns a new superuser instance.

        Parameters:
            email (str): The unique email address for the superuser.
            username (str): The username for the superuser.
            password (str, optional): The password for the superuser. Defaults to None.

        Returns:
            Accounts: A new superuser instance with admin privileges.

        Raises:
            ValueError: If email or username is not provided.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_customer_avatar_path(self, filename):
    return f'customer_profile_picture/{self.pk}/{filename}'
class Accounts(AbstractBaseUser):
    """
    Custom user model for managing customer and admin accounts in the e-commerce application.

    This model supports email-based authentication and includes additional fields
    for profile management. It extends Django's AbstractBaseUser and integrates
    with the custom `AccountsManager` for user creation.

    Attributes:
        email (EmailField):
            - Unique email address for the user.
            - Acts as the primary identifier for authentication.

        username (CharField):
            - The unique username for the user.

        first_name (CharField):
            - The user's first name. Optional.

        middle_name (CharField):
            - The user's middle name. Optional.

        last_name (CharField):
            - The user's last name. Optional.

        phone_no (CharField):
            - The user's phone number.

        profile_picture (ResizedImageField):
            - The user's profile picture, resized to [244x244].
            - Stored in a custom path using `get_customer_avatar_path`.

        skinType (CharField):
            - The user's skin type (e.g., Normal, Oily, Dry, etc.).
            - Optional field with predefined choices.

        block (BooleanField):
            - Indicates whether the account is blocked. Defaults to False.

        date_joined (DateTimeField):
            - The date and time when the account was created.

        last_login (DateTimeField):
            - The date and time when the user last logged in.

        is_active (BooleanField):
            - Indicates whether the account is active. Defaults to True.

        is_admin (BooleanField):
            - Indicates whether the user has admin privileges.

        is_staff (BooleanField):
            - Indicates whether the user has staff privileges.

        is_superuser (BooleanField):
            - Indicates whether the user has superuser privileges.

    Methods:
        __str__():
            - Returns the username as the string representation of the user.

        has_perm(perm, obj=None):
            - Checks if the user has the specified permission. Always returns True for admins.

        has_module_perms(app_label):
            - Checks if the user has permissions for the specified app. Always returns True for admins.

    Meta:
        verbose_name (str): A human-readable singular name for the model.
        verbose_name_plural (str): A human-readable plural name for the model.

    Example Usage:
        # Creating a regular user
        user = Accounts.objects.create_user(
            email="user@example.com",
            username="user123",
            password="securepassword123"
        )

        # Checking user attributes
        print(user.is_active)  # Output: True

        # Checking if the user is an admin
        print(user.is_admin)  # Output: False
    """

    SKIN_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('oily', 'Oily'),
        ('dry', 'Dry'),
        ('combination', 'Combination'),
        ('sensitive', 'Sensitive'),
    ]

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Email Address",
        null=False,
        blank=False
    )
    username = models.CharField(
        max_length=50,
        verbose_name="Username",
        null=False,
        blank=False
    )
    first_name = models.CharField(max_length=50, verbose_name="First Name", blank=True)
    middle_name = models.CharField(max_length=50, verbose_name="Middle Name", blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Last Name", blank=True)
    phone_no = models.CharField(max_length=15, verbose_name="Phone Number", blank=True)
    profile_picture = ResizedImageField(
        size=[244, 244],
        upload_to=get_customer_avatar_path,
        blank=True,
        null=True
    )
    skinType = models.CharField(
        max_length=20,
        choices=SKIN_TYPE_CHOICES,
        blank=True,
        verbose_name="Skin Type"
    )
    block = models.BooleanField(
        default=False,
        verbose_name="Block Account"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Joined",
        null=False,
        blank=False
    )
    last_login = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Login"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="Admin"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Staff"
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Superuser"
    )

    objects = AccountsManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """
        Returns the string representation of the user, which is the username.

        Returns:
            str: The user's username.
        """
        return self.username

    def has_perm(self, perm, obj=None):
        """
        Checks if the user has a specific permission. Admin users always return True.

        Parameters:
            perm (str): The permission to check.
            obj (object, optional): The object for which the permission is checked.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Checks if the user has permissions for the specified app. Admin users always return True.

        Parameters:
            app_label (str): The label of the app to check.

        Returns:
            bool: True if the user has permissions for the app, False otherwise.
        """
        return True

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


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
    
class Notification(models.Model):
    
    title = models.CharField(max_length=2000,null=False,blank=False)
    description = models.TextField(null=True,blank=True)
    link = models.CharField(max_length=2000,null=True,blank=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Title:{self.title} - Created By:{self.updated_by} - Created At{self.created_at}"
    
class NotificationTo(models.Model):

    to = models.ForeignKey(Accounts,on_delete=models.CASCADE,related_name='notification_to')
    notification = models.ForeignKey(Notification,on_delete=models.CASCADE,related_name='notification')
    read = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Notification To"
        verbose_name_plural = "Notifications To"

    def __str__(self):
        return f"Created By:{self.updated_by} - Created At {self.created_at}"

class EmailAccounts(models.Model):
    name = models.CharField(max_length=100, help_text="Friendly name for this email account")
    email_address = models.EmailField(max_length=100, help_text="Email address to send from")
    smtp_server = models.CharField(max_length=100, help_text="SMTP server address")
    smtp_port = models.IntegerField(default=587, help_text="SMTP server port")
    username = models.CharField(max_length=100, help_text="SMTP username",null=True,blank=True)
    password = models.CharField(max_length=100, help_text="SMTP password")
    use_tls = models.BooleanField(default=True, help_text="Use TLS for connection")
    use_ssl = models.BooleanField(default=False, help_text="Use SSL for connection")
    is_active = models.BooleanField(default=True, help_text="Is this account active?")
    
    PURPOSE_CHOICES = [
        ('marketing', 'Marketing Emails'),
        ('transactional', 'Transactional Emails'),
        ('notification', 'Notification Emails'),
        ('support', 'Support Emails'),
        ('auth','Authentication'),
        ('other', 'Other'),
    ]

    class Meta:
        verbose_name = "Email Account"
        verbose_name_plural = "Email Accounts"
    
    def __str__(self):
        return str(self.pk)

class EmailTemplate(models.Model):
    """Model to store email templates"""
    name = models.CharField(max_length=100, help_text="Template name")
    subject = models.CharField(max_length=200, help_text="Email subject")
    body_text = models.TextField(help_text="Plain text email body")
    body_html = models.TextField(blank=True, null=True, help_text="HTML email body")
    
    PURPOSE_CHOICES = [
        ('marketing', 'Marketing Emails'),
        ('transactional', 'Transactional Emails'),
        ('notification', 'Notification Emails'),
        ('support', 'Support Emails'),
        ('auth','Authentication'),
        ('other', 'Other'),
    ]
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, help_text="Template purpose")
    
    def __str__(self):
        return str(self.pk)

    