from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
import hashlib
from system.models import Accounts
# Create your models here.

# Admin Positions Model
class AdminPositions(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


def get_admin_avatar_path(instance, filename):
    return f'admin_profile_picture/{instance.admin_unique_id}/{filename}'

class BusinessAdminUser(models.Model):
    '''
        admin will login with the unique id. The unique id will be taken input from the user.
    '''
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    admin_unique_id=models.CharField(null=False,blank=False,max_length=1000,primary_key=True)
    admin_full_name=models.CharField(null=False,blank=False,max_length=1000)
    admin_user_name = models.CharField(null=True,blank=True,max_length=1000)
    admin_avatar=ResizedImageField(size=[244,244],upload_to=get_admin_avatar_path,blank=True, null=True)
    admin_position=models.ForeignKey(AdminPositions,null=True,blank=True,on_delete=models.CASCADE)
    admin_email=models.EmailField(null=False,blank=False)
    admin_contact_no=models.CharField(null=True,blank=True,max_length=20)
    admin_account_created_at=models.DateTimeField(null=False,blank=False,auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name="Admin User"
        verbose_name_plural="Admin Users"
    
    def __str__(self):
        return str(self.admin_unique_id)
    
    def generate_and_save_unique_id(self):
        
        existing_admins_count = BusinessAdminUser.objects.all().count()

        full_name = self.admin_full_name.replace(' ','_')
        base_sku = f"{full_name.upper()}_{self.admin_user_name.upper()}_{existing_admins_count+1}"
        unique_hash = hashlib.md5(base_sku.encode()).hexdigest()[:6]
        self.admin_unique_id = f"{base_sku}_{unique_hash.upper()}"
    
    def save(self, *args, **kwargs):
        #if newly created only then
        if not self.pk or self._is_admin_related_field_updated():
            self.generate_and_save_unique_id()
        
        super(BusinessAdminUser, self).save(*args, **kwargs)
    
    def _is_admin_related_field_updated(self):
        """Check if fields affecting admin unique id generation have been updated."""
        if not self.pk:
            return False

        # Get the current state from the database
        current = BusinessAdminUser.objects.get(pk=self.pk)
        return (
            current.admin_full_name != self.admin_full_name 
        )


# Permission Model
class AdminPermissions(models.Model):
    
    #choices
    CREATE = "create"
    DELETE = "delete"
    UPDATE= "update"
    VIEW = "view"

    '''All the permissions for admin users'''
    permission_name = models.CharField(max_length=100, unique=True)
    permission_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.permission_name

    def __lt__(self, other):
        return self.permission_name < other.permission_name


# AdminRolePermissions (Associative Entity for Role and Permission)
class AdminRolePermission(models.Model):
    '''Admin role permissions are stored here'''
    role = models.ForeignKey(AdminPositions, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(AdminPermissions, on_delete=models.CASCADE, related_name='role_permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.permission_name}"
    
class AdminUserRole(models.Model):

    user = models.OneToOneField(Accounts, on_delete=models.CASCADE, related_name='admin_role')
    role = models.ForeignKey(AdminPositions, on_delete=models.CASCADE, related_name='users',null=True,blank=True)
    updated_by = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


# Audit Log Model
class ActivityLog(models.Model):
    '''Activity Logs are stored in the models.
        Actions are stored as strings. Actions are written by devs within functions    
        Details are stored in JSON if the dev decides to store more informations.
    '''
    activity_done_by_business_admin = models.ForeignKey(BusinessAdminUser, on_delete=models.CASCADE, related_name='audit_logs',null=True,blank=True)
    activity_done_by_dev_admin = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True,blank=True)
    action = models.CharField(max_length=500)
    details = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_done_by_admin.admin_full_name} - {self.activity_done_by_admin.admin_unique_id} - {self.action}"


# Session Model
class Session(models.Model):
    '''Sessions of every admin logins are stored in this model.'''
    admin = models.ForeignKey(BusinessAdminUser, on_delete=models.CASCADE, related_name='sessions')
    session_token = models.CharField(max_length=255, unique=True,blank=True,null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    device_details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.admin.admin_email} - {self.session_token}"