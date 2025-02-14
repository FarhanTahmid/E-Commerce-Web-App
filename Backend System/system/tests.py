from django.test import TestCase
from unittest.mock import patch
from datetime import datetime
from .models import ErrorLogs
from .manage_error_log import ManageErrorLog

class TestCreateErrorLog(TestCase):
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