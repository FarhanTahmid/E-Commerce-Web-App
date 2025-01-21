from products.models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.models import *
from business_admin.models import *
from django.utils import timezone
from django.contrib.auth.models import User

class SystemLogs:

    def updated_by(request,model_instance):

        """
        Update the 'updated_by' field of a model instance with detailed exception handling.

        This function updates the 'updated_by' field of a given model instance based on the type of user making the request.
        It handles various errors that might occur during the process, logging each error for further analysis.

        Args:
            request (Request): The request object containing the user information.
            model_instance (Model): The model instance to be updated.

        Returns:
            tuple:
                - bool: `True` if the 'updated_by' field was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = updated_by(request, some_model_instance)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating 'updated by field' for system logs! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating 'updated by field' for system logs! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating 'updated by field' for system logs! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating 'updated by field' for system logs! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        #checking type of user
        try:
            user = User.objects.get(username = request.user.username)
            if user.is_superuser:
                user_type = {
                "user_type": " Developer - Superuser",
                "username": request.user.username,
                "date": timezone.now().isoformat() 
                }
            else:
                try:
                    business_admin = BusinessAdminUser.objects.get(user=user)
                    if business_admin:
                        user_type = {
                        "user_type": "Business Admin",
                        "username": business_admin.admin_full_name,
                        "unique_id":business_admin.admin_unique_id,
                        "date": timezone.now().isoformat() 
                        }
                except:
                    return False, "Error while updating logs"
            
            current_data = model_instance.updated_by or {}
            if isinstance(current_data, dict):
                current_data.update(user_type)
            else:
                current_data = user_type
            model_instance.updated_by = current_data
            model_instance.save()

            return True, "Updated logs successfully"
   
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating 'updated by field' for system logs! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating 'updated by field' for system logs! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating 'updated by field' for system logs! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while updating 'updated by field' for system logs! Please try again later.")