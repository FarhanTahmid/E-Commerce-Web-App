from django.test import TestCase,RequestFactory
from unittest.mock import patch
from datetime import datetime
from .models import ErrorLogs,Notification,Accounts,NotificationTo
from django.contrib.auth import get_user_model
from .manage_error_log import ManageErrorLog
from .manage_system import SystemManagement


User = get_user_model()

class TestCreateErrorLog(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            username='user1',
            password='testpass123'
        )
        self.user1.save()
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            username='user2',
            password='testpass123'
        )
        self.user2.save()

        self.notification1 = Notification.objects.create(
            title = "11"
        )
        self.notification1_to1 = NotificationTo.objects.create(to=self.user1,notification=self.notification1)
        self.notification1_to2 = NotificationTo.objects.create(to=self.user2,notification=self.notification1)


        self.notification2 = Notification.objects.create(
            title = "12"
        )
        self.notification2_to1 = NotificationTo.objects.create(to=self.user1,notification=self.notification2)

    def _create_mock_dev_user(self):
        """ Helper method to create a mock user """
        return Accounts.objects.create(
            email='user@example.com',
            username='user',
            is_superuser = True,
            password='1234',
        )
    
    def test_create_error_log_success(self):
        """
        Test creating an error log successfully.
        """
        error_type = "TestError"
        error_message = "This is a test error message."

        # Call the function
        result = ManageErrorLog.create_error_log(error_type, error_message)

        # Check if the log was created
        self.assertTrue(result, "The function should return True on successful creation of an error log.")
        self.assertEqual(ErrorLogs.objects.count(), 1, "There should be exactly one error log in the database.")

        # Verify the contents of the log
        error_log = ErrorLogs.objects.first()
        self.assertEqual(error_log.error_type, error_type, "The error type does not match.")
        self.assertEqual(error_log.error_message, error_message, "The error message does not match.")
        self.assertIsInstance(error_log.timestamp, datetime, "The timestamp should be a valid datetime object.")

    @patch('system.models.ErrorLogs.save', side_effect=Exception("Database save error"))
    def test_create_error_log_save_exception(self, mock_save):
        """
        Test handling of exceptions during error log creation.
        """
        error_type = "TestError"
        error_message = "This is a test error message."

        # Call the function
        result = ManageErrorLog.create_error_log(error_type, error_message)

        # Ensure the function handles the exception gracefully
        self.assertIsNone(result, "The function should return None if an exception occurs during save.")

        # Verify no log was created
        self.assertEqual(ErrorLogs.objects.count(), 0, "No error logs should be created if an exception occurs.")

    def test_fetch_user_notification(self):

        """
        Test for fetching user notifications
        """

        request = self.factory.post('/product/product_discount/fetch/')
        request.user = self._create_mock_dev_user()
        success,message = SystemManagement.fetch_notifications_of_user(user_name=self.user1.username,read="f")
        print(success)
        print(message)

    