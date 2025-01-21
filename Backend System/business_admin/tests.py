from django.test import TestCase,RequestFactory
from .admin_management import AdminManagement
from .models import AdminPositions
from django.contrib.auth.models import User
from .models import BusinessAdminUser

# Create your tests here.
class BusinessAdminTest(TestCase):


    def setUp(self):
        self.factory = RequestFactory()
        self.adminposition1 = AdminPositions.objects.create(name="Manager",description="Manage of company")

    def _create_mock_dev_user(self):
        """ Helper method to create a mock user """
        return User.objects.create(username='testuser', is_superuser=True)

    def _create_mock_businessadmin_user(self):
        user = User.objects.create(username='testuser2', is_superuser=False)
        BusinessAdminUser.objects.create(user=user,admin_full_name="testuser2",admin_position=self.adminposition1).save()
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
        #request.user = self._create_mock_dev_user()
        request.user = self._create_mock_businessadmin_user()
        success, message = AdminManagement.create_admin_position(request,name="Owner",description="Is Owner")
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