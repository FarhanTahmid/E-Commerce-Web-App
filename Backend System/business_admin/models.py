from django.db import models
from django_resized import ResizedImageField
# Create your models here.

# Admin Positions Model
class AdminPositions(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def get_admin_avatar_path(instance, filename):
    return f'admin_profile_picture/{instance.admin_unique_id}/{filename}'

class BusinessAdminUser(models.Model):
    '''
        admin will login with the unique id. The unique id will be taken input from the user.
    '''
    admin_unique_id=models.CharField(null=False,blank=False,max_length=50,primary_key=True)
    admin_full_name=models.CharField(null=False,blank=False,max_length=100)
    admin_avatar=ResizedImageField(size=[244,244],upload_to=get_admin_avatar_path,blank=True, null=True)
    admin_position=models.OneToOneField(AdminPositions,null=False,blank=False,on_delete=models.CASCADE)
    admin_email=models.EmailField(null=True,blank=True)
    admin_contact_no=models.CharField(null=True,blank=True,max_length=20)
    admin_is_staff=models.BooleanField(null=False,blank=False,default=False)
    admin_is_superuser=models.BooleanField(null=False,blank=False,default=False)
    admin_account_created_at=models.DateTimeField(null=False,blank=False,auto_now_add=True)
    last_login_at=models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name="Admin User"
        verbose_name_plural="Admin Users"
    
    def __str__(self):
        return str(self.admin_unique_id)


# Permission Model
class AdminPermissions(models.Model):
    '''All the permissions for admin users'''
    permission_name = models.CharField(max_length=100, unique=True)
    permission_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.permission_name


# AdminRolePermissions (Associative Entity for Role and Permission)
class AdminRolePermission(models.Model):
    '''Admin role permissions are stored here'''
    role = models.ForeignKey(AdminPositions, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(AdminPermissions, on_delete=models.CASCADE, related_name='role_permissions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


# Audit Log Model
class ActivityLog(models.Model):
    '''Activity Logs are stored in the models.
        Actions are stored as strings. Actions are written by devs within functions    
        Details are stored in JSON if the dev decides to store more informations.
    '''
    activity_done_by_admin = models.ForeignKey(BusinessAdminUser, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=500)
    details = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.admin_email} - {self.action}"


# Session Model
class Session(models.Model):
    '''Sessions of every admin logins are stored in this model.'''
    admin = models.ForeignKey(BusinessAdminUser, on_delete=models.CASCADE, related_name='sessions')
    session_token = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    device_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.admin.admin_email} - {self.session_token}"