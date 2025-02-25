from django.test import TestCase,RequestFactory
from django.contrib.auth import get_user_model
from .models import DeliveryTime
from .order_management import OrderManagement
from .models import Accounts

User = get_user_model()

class OrderTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            username='user1',
            password='testpass123'
        )

        self.delivery_time1 = DeliveryTime.objects.create(
            delivery_name= "Inside dhaka",
            estimated_delivery_time = "7 days"
        )
        self.delivery_time2 = DeliveryTime.objects.create(
            delivery_name= "Outside dhaka",
            estimated_delivery_time = "10 days"
        )
        self.delivery_time3 = DeliveryTime.objects.create(
            delivery_name= "Internation",
            estimated_delivery_time = "1 months"
        )

    def _create_mock_dev_user(self):
        """ Helper method to create a mock user """
        return Accounts.objects.create(
            email='user@example.com',
            username='user',
            is_superuser = True,
            password='1234',
        )
    
    def test_fetch_delivery_time(self):

        request = self.factory.get('/delivery/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.fetch_delivery_time(delivery_pk=self.delivery_time1.pk)
        self.assertTrue(success,"Fetched")
        self.assertEqual(message,"Fetched Successfully")

    def test_create_delivery_time(self):

        request = self.factory.get('/delivery/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.create_delivery_time(request,"Inside dhaka","5 days")
        self.assertFalse(success,"Not created")
        self.assertEqual(message, "Delivery Time with this name already exists")

        success,message = OrderManagement.create_delivery_time(request,"Outside omar","pp")
        self.assertTrue(success,"Created")

    def test_update_delivery_time(self):

        request = self.factory.get('/delivery/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.update_delivery_time(request,self.delivery_time3.pk,"Indianaa","opop")
        self.assertTrue(success,"Updated")

    def test_delete_delivery_time(self):

        request = self.factory.get('/delivery/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = OrderManagement.delete_delivery_time(request,self.delivery_time2.pk)
        self.assertTrue(success,"Deleted")