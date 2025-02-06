from django.test import TestCase,RequestFactory
from .admin_management import AdminManagement
from .models import *
from system.models import *
from .models import BusinessAdminUser

# Create your tests here.
class BusinessAdminTest(TestCase):


    def setUp(self):
        self.factory = RequestFactory()
        self.adminposition1 = AdminPositions.objects.create(name="Manager",description="Manage of company")
        self.adminposition2 = AdminPositions.objects.create(name="Owner",description="Ownerrr")

        self.businessadmin1 = BusinessAdminUser.objects.create(admin_full_name="SAMI",admin_position=self.adminposition2,admin_email="sak@gmail.com",admin_user_name='sak')
        self.businessadmin1.save()
        self.user = Accounts(username='sak',password='1234',email="sak@gmail.com",is_admin=True,is_superuser=True)
        self.user.save()

        self.businessadmin2 = BusinessAdminUser.objects.create(admin_full_name="RAFI",admin_position=self.adminposition1,admin_email="rafi@gmail.com",admin_user_name='rafi')
        self.businessadmin2.save()
        self.user2 = Accounts(username='rafi',password='1234',email="rafi@gmail.com",is_admin=True)
        self.user2.save()

        self.adminpermisison1 = AdminPermissions.objects.create(permission_name=AdminPermissions.CREATE)
        self.adminpermisison2 = AdminPermissions.objects.create(permission_name=AdminPermissions.UPDATE)

        self.adminrolepermission1 = AdminRolePermission.objects.create(role=self.adminposition1,permission=self.adminpermisison1)#create - manager
        self.adminrolepermission2 = AdminRolePermission.objects.create(role=self.adminposition2,permission=self.adminpermisison2)#update - owner
        self.adminrolepermission3 = AdminRolePermission.objects.create(role=self.adminposition2,permission=self.adminpermisison1)#create - owner

        self.adminuserrole1 = AdminUserRole.objects.create(user=self.user,role=self.adminposition2)#owner
        self.adminuserrole2 = AdminUserRole.objects.create(user=self.user2,role=self.adminposition1)#manager


    def _create_mock_dev_user(self):
        """ Helper method to create a mock user """
        return Accounts.objects.create(
            email='user@example.com',
            username='user',
            is_superuser = True,
            password='1234',
        )

    def _create_mock_businessadmin_user(self):
        user = Accounts.objects.create(username='sami', is_superuser=True,is_admin = True,email='sami@gmail.com',password='1234')
        user.save()
        businessadmin_user = BusinessAdminUser.objects.create(admin_full_name="sami",admin_position=self.adminposition1,admin_email='sami@gmail.com',admin_user_name='sami')
        businessadmin_user.save()
        return user

    def test_fetch_admin_postion(self):
        """
        Test for fetching admin posiiton
        """

        #using name
        success, message = AdminManagement.fetch_admin_position(name = self.adminposition1.name)
        self.assertTrue(success,"Admin Position should be fetched successfully")
        self.assertEqual(message,"Admin position fetched successfully!","Success message is incorrect")

        #all
        success, message = AdminManagement.fetch_admin_position()
        self.assertTrue(success,"Admin Position should be created successfully")
        self.assertEqual(message,"All Admin positions fetched successfully!","Success message is incorrect")

    def test_create_admin_position(self):
        """
        Test for creating admin position
        """
        request = self.factory.post('/admin_positions/create/')
        request.user = self._create_mock_dev_user()
        #request.user = self._create_mock_businessadmin_user()
        success, message = AdminManagement.create_admin_position(request,name="Owner55",description="Is Owner55")
        self.assertTrue(success,"Admin Position should be created successfully")
        self.assertEqual(message,"Admin position created successfully","Success message is incorrect")

        #business admin user
        success, message = AdminManagement.create_admin_position(request,name="Owner2",description="Is Owner")
        self.assertTrue(success,"Admin Position should be created successfully")
        self.assertEqual(message,"Admin position created successfully","Success message is incorrect")

        #duplicate
        success, message = AdminManagement.create_admin_position(request,name="Owner",description="Is Owner")
        self.assertFalse(success,"Admin Position should not be created successfully")
        self.assertEqual(message,"Admin position with this name already exists!","Error message is incorrect")

    def test_update_admin_position(self):
        """
        Test for updating admin position
        """
        request = self.factory.post('/admin_positions/update/')
        request.user = self._create_mock_dev_user()
        #request.user = self._create_mock_businessadmin_user()
        success, message = AdminManagement.update_admin_position(request,admin_position_pk=self.adminposition1.pk,name="Manager2")
        self.assertTrue(success,"Admin Position should be updated successfully")
        self.assertTrue(self.adminposition1.name,"Manager2")
        self.assertEqual(message,"Admin position successfully updated","Success message is incorrect")

    def test_delete_admin_position(self):
        """
        Test for deleting admin position
        """
        request = self.factory.post('/admin_positions/delete/')
        request.user = self._create_mock_dev_user()
        #request.user = self._create_mock_businessadmin_user()
        success, message = AdminManagement.delete_admin_position(request,self.adminposition2.pk)
        self.assertTrue(success,"Admin Position should be deleted successfully")
        self.assertEqual(message,"Admin position deleted successfully")

        #deleting again
        # success, message = AdminManagement.delete_admin_position(request,self.adminposition2.pk)
        # self.assertFalse(success,"Admin Position should not be deleted successfully")
        # self.assertEqual(message,"An unexpected error occurred while deleting admin position! Please try again later.")

    #Business admin test
    def test_fetch_business_admin(self):
        """
        Test for fetching business admins
        """

        #all
        request = self.factory.post('/admins/fetch/')
        request.user = self._create_mock_dev_user()
        #request.user = self._create_mock_businessadmin_user()
        success, message = AdminManagement.fetch_business_admin_user()
        self.assertTrue(success,"Admin should be fetched successfully")
        self.assertEqual(message,"All Business Admin users fetched successfully","Success message is incorrect")

    def test_create_business_admin(self):
        """
        Test for creating business admins
        """
        
        success, message = AdminManagement.create_business_admin_user(admin_full_name="SAMI",
                                                                      password='2186',admin_email='saki@gmail.com',is_superuser=True)
        self.assertTrue(success,"Business Admin should be created successfully")
        self.assertEqual(message,"Business Admin created successfully","Success message is incorrect")

        #same email
        success, message = AdminManagement.create_business_admin_user(admin_full_name="SAMI",
                                                                      password='2186',admin_email='saki@gmail.com')
        self.assertFalse(success,"Business Admin should not be created successfully")
        self.assertEqual(message,"Admin with this email already exists","Error message is incorrect")

    def test_update_business_admin(self):
        """
        Test for updating business admins
        """
        request = self.factory.post('/admins/update/')
        #request.user = self._create_mock_dev_user()
        request.user = self._create_mock_businessadmin_user()
        success, message = AdminManagement.update_business_admin_user(request,admin_unique_id="SAMI_SAK_1_1C4759",
                                                                 admin_full_name="rafi",admin_email='rrr@gmail.com',
                                                                 admin_contact_no="01306413841")
        self.assertTrue(success,"business admin should be successfully updated")
        self.assertEqual(message,"Business Admin successfully updated","Success message is incorrect")
    
    def test_update_password_reset(self):
        """
        Test for reseting the password
        """
        request = self.factory.post('/admins/reset_password/')
        #request.user = self._create_mock_dev_user()
        request.user = self._create_mock_businessadmin_user()
        success,message = AdminManagement.reset_business_admin_user_password(request,request.user.email,"8585")
        self.assertTrue(success,"Password should be successfully reset")
        self.assertEqual(message,"Password reset successfull","Success message is incorrect")


    def test_delete_business_admin(self):
        """
        Test for deleting business admins
        """
        request = self.factory.post('/admins/delete/')
        request.user = self._create_mock_dev_user()
        #request.user = self._create_mock_businessadmin_user()
        success, message = AdminManagement.delete_business_admin_user(request,"SAMI_SAK_1_1C4759")
        self.assertTrue(success,"business admin should be successfully deleted")
        self.assertEqual(message,"Admin deleted successfully","Success message is incorrect")

        #deleteing again
        # success, message = AdminManagement.delete_business_admin_user(request,"SAMI_SAMI2186_1_a98961")
        # self.assertFalse(success,"business admin should not be found")
        # self.assertEqual(message,"An unexpected error occurred while deleting admin user! Please try again later.","Error message is incorrect")

    #admin permissions
    def test_fetch_admin_permissions(self):
        """
        Test for fetching admin permissions
        """
        #all
        request = self.factory.post('/admins/fetch-position/')
        request.user = self._create_mock_dev_user()
        success,message = AdminManagement.fetch_admin_permissions()
        self.assertTrue(success,"Admin permission fetched should be successfully")
        self.assertEqual(message,"All permissions fetched successfully")

        #name
        success,message = AdminManagement.fetch_admin_permissions(permission_name=self.adminpermisison1.permission_name)
        self.assertTrue(success,"Admin permission fetched should be successfully")
        self.assertEqual(message,"Permission fetched successfully")

    def test_create_admin_permissions(self):
        """
        Test for creating admin position
        """

        #exisiting
        request = self.factory.post('/admins/create-admin-permissoins/')
        request.user = self._create_mock_dev_user()
        success,message = AdminManagement.create_admin_permissions(request,self.adminpermisison1.permission_name)
        self.assertFalse(success,"Admin permission should not be successfully created")
        self.assertEqual(message,"Admin permission with this name already exists")

        #new
        success,message = AdminManagement.create_admin_permissions(request,AdminPermissions.DELETE)
        self.assertTrue(success,"Admin permission should be successfully created")
        self.assertEqual(message,"Admin permission created successfully")

    def test_update_admin_permissions(self):
        """
        Test for updating admin permissions
        """
        #existing
        request = self.factory.post('/admins/update-admin-permissions/')
        request.user = self._create_mock_dev_user()
        success,message = AdminManagement.update_admin_permissions(request,self.adminpermisison2.pk,AdminPermissions.CREATE)
        self.assertFalse(success,"Admin permission should not be successfully updated")
        self.assertEqual(message,"Permission with this name already exists")

        #new
        success,message = AdminManagement.update_admin_permissions(request,self.adminpermisison2.pk,AdminPermissions.DELETE)
        self.assertTrue(success,"Admin permission should be successfully updated")
        self.assertEqual(message,"Admin permissions updated successfully")

    def test_delete_admin_permissions(self):
        """
        Test for deleting admin permissions
        """
        request = self.factory.post('/admins/delete-admin-permissions/')
        request.user = self._create_mock_dev_user()
        success,message = AdminManagement.delete_admin_permissions(request,self.adminpermisison2.pk)
        self.assertTrue(success,"Admin permission should be successfully deleted")
        self.assertEqual(message,"Admin permission deleted successfully")

    def test_fetch_position_of_admin(self):
        """
        Test for fetching postiion of admin
        """
        request = self.factory.post('/admins/fetch-admin-postiion/')
        request.user = self._create_mock_dev_user()
        success,message = AdminManagement.fetch_postion_of_admin(request,self.businessadmin1.admin_user_name)
        self.assertTrue(success,"Admin position should be successfully fetched")
        self.assertEqual(message,"Fetched successfully")
    
    def test_add_or_update_position_of_admin(self):
        """
        test for adding position of admin
        """
        request = self.factory.post('/admins/add-admin-postiion/')
        request.user = self._create_mock_dev_user()
        success,message = AdminManagement.add_or_update_admin_position(request,self.businessadmin1.admin_user_name,self.adminposition2.pk)
        self.assertTrue(success,"Admin position should be successfully added")
        self.assertEqual(message,"Successfull")

        #update
        success,message = AdminManagement.add_or_update_admin_position(request,self.businessadmin1.admin_user_name,self.adminposition1.pk)
        self.assertTrue(success,"Admin position should be successfully added")
        self.assertEqual(message,"Successfull")

    def test_delete_position_of_admin(self):
        """
        Test for deleting position of admin
        """
        request = self.factory.post('/admins/delete-admin-postiion/')
        request.user = self._create_mock_dev_user()
        success,message = AdminManagement.remove_position_of_admin(request,self.businessadmin1.admin_user_name)
        self.assertTrue(success,"Admin position should be successfully removed")
        self.assertEqual(message,"Admin position removed successfully")
        
    #test admin role permissions
    def test_fetch_admin_role_permissions(self):
        """
        Test for fetching admin role permissions
        """
        request = self.factory.post('/admins/fetch-role-permissions/')
        request.user = self._create_mock_dev_user()

        #all
        success,message = AdminManagement.fetch_admin_role_permission()
        self.assertTrue(success,"Admin role permissions should be successfully fetched")
        self.assertEqual(message,"All fetched successfully")
        
        #using pk
        success,message = AdminManagement.fetch_admin_role_permission(admin_role_permission_pk=self.adminrolepermission1.pk)
        self.assertTrue(success,"Admin role permissions should be successfully fetched")
        self.assertEqual(message,"Fetched successfully")

        #using permission pk
        success,message = AdminManagement.fetch_admin_role_permission(admin_permission_pk=self.adminpermisison1.pk)
        self.assertTrue(success,"Admin role permissions should be successfully fetched")    
        self.assertEqual(message,"Fetched successfully")

        #using role pk
        success,message = AdminManagement.fetch_admin_role_permission(admin_position_pk=self.adminposition2.pk)
        self.assertTrue(success,"Admin role permissions should be successfully fetched")    
        self.assertEqual(message,"Fetched successfully")

    def test_create_admin_role_position(self):
        """
        Test for creating admin role permissions
        """
        request = self.factory.post('/admins/create-role-permissions/')
        request.user = self._create_mock_dev_user()

        #existing
        success,message = AdminManagement.create_admin_role_permission(request,self.adminposition2.pk,[self.adminpermisison2.pk,self.adminpermisison1.pk])
        self.assertTrue(success,"Admin role permissions should be successfully created")
        self.assertEqual(message,"Already exists")

        #new
        success,message = AdminManagement.create_admin_role_permission(request,self.adminposition1.pk,[self.adminpermisison2.pk,self.adminpermisison1.pk])
        self.assertTrue(success,"Admin role permissions should be successfully created")
        self.assertEqual(message,"Created successfully")

    def test_update_admin_role_position(self):
        """
        Test for updating admin role permissions
        """
        request = self.factory.post('/admins/update-role-permissions/')
        request.user = self._create_mock_dev_user()

        #existing
        success,message = AdminManagement.update_admin_role_permission(request,self.adminposition2.pk,[self.adminpermisison2.pk,self.adminpermisison1.pk])
        self.assertTrue(success,"Admin role permissions should be successfully updated")
        self.assertEqual(message,"Updated successfully")

        #new
        success,message = AdminManagement.update_admin_role_permission(request,self.adminposition1.pk,[self.adminpermisison1.pk])
        self.assertTrue(success,"Admin role permissions should be successfully updated")
        self.assertEqual(message,"Updated successfully")

    def test_delete_admin_role_position(self):

        """
        Test for deleting admin role permissions
        """
        request = self.factory.post('/admins/delete-role-permissions/')
        request.user = self._create_mock_dev_user()

        #existing
        success,message = AdminManagement.delete_admin_role_permission(request,self.adminposition1.pk)#manager
        self.assertTrue(success,"Admin role permissions should be successfully deleted")
        self.assertEqual(message,"Deleted successfully")

        #new
        success,message = AdminManagement.delete_admin_role_permission(request,self.adminposition1.pk)
        self.assertTrue(success,"Admin role permissions should be successfully deleted")
        self.assertEqual(message,"Deleted successfully")







