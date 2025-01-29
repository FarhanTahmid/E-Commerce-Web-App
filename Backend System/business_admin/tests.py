from django.test import TestCase,RequestFactory
from .admin_management import AdminManagement
from .models import AdminPositions
from system.models import *
from .models import BusinessAdminUser

# Create your tests here.
class BusinessAdminTest(TestCase):


    def setUp(self):
        self.factory = RequestFactory()
        self.adminposition1 = AdminPositions.objects.create(name="Manager",description="Manage of company")
        self.adminposition2 = AdminPositions.objects.create(name="Owner",description="Ownerrr")
        self.businessadmin1 = BusinessAdminUser.objects.create(admin_full_name="SAMI",admin_position=self.adminposition2,admin_email="sak@gmail.com",admin_user_name='sak')

    def _create_mock_dev_user(self):
        """ Helper method to create a mock user """
        return Accounts.objects.create(
            email='user@example.com',
            username='user',
            is_superuser = True,
            password='1234',
        )

    def _create_mock_businessadmin_user(self):
        user = Accounts.objects.create(username='testuser2', is_superuser=True,is_admin = True,email='sami@gmail.com',password='1234')
        BusinessAdminUser.objects.create(admin_full_name="testuser2",admin_position=self.adminposition1,admin_email='sami@gmail.com',admin_user_name='sami').save()
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
                                                                      password='2186',admin_position_pk=self.adminposition2.pk,admin_email='saki@gmail.com')
        self.assertTrue(success,"Business Admin should be created successfully")
        self.assertEqual(message,"Business Admin created successfully","Success message is incorrect")

        #same username
        success, message = AdminManagement.create_business_admin_user(admin_full_name="SAMI",
                                                                      password='2186',admin_position_pk=self.adminposition2.pk)
        self.assertFalse(success,"Business Admin should not be created successfully")
        self.assertEqual(message,"Admin with this username exists","Error message is incorrect")

    def test_update_business_admin(self):
        """
        Test for updating business admins
        """
        print(self.businessadmin1.admin_unique_id)
        request = self.factory.post('/admins/update/')
        request.user = self._create_mock_dev_user()
        #request.user = self._create_mock_businessadmin_user()
        success, message = AdminManagement.update_business_admin_user(request,admin_unique_id="SAMI_SAMI2186_1_A98961",
                                                                 admin_full_name="rafi",admin_position_pk=self.adminposition2.pk,admin_email='saki@gmail.com',
                                                                 admin_contact_no="01306413841")
        self.assertTrue(success,"business admin should be successfully updated")
        self.assertEqual(message,"Business Admin successfully updated","Success message is incorrect")
    
    def test_update_password_reset(self):
        """
        Test for reseting the password
        """
        request = self.factory.post('/admins/reset_password/')
        request.user = self._create_mock_dev_user()
        #request.user = self._create_mock_businessadmin_user()
        success,message = AdminManagement.reset_business_admin_user_password(request,"sami2186","8585")
        self.assertTrue(success,"Password should be successfully reset")
        self.assertEqual(message,"Password reset successfull","Success message is incorrect")


    def test_delete_business_admin(self):
        """
        Test for deleting business admins
        """
        request = self.factory.post('/admins/delete/')
        request.user = self._create_mock_dev_user()
        #request.user = self._create_mock_businessadmin_user()
        success, message = AdminManagement.delete_business_admin_user(request,"SAMI_SAMI2186_1_A98961")
        self.assertTrue(success,"business admin should be successfully deleted")
        self.assertEqual(message,"Admin deleted successfully","Success message is incorrect")

        #deleteing again
        # success, message = AdminManagement.delete_business_admin_user(request,"SAMI_SAMI2186_1_a98961")
        # self.assertFalse(success,"business admin should not be found")
        # self.assertEqual(message,"An unexpected error occurred while deleting admin user! Please try again later.","Error message is incorrect")


