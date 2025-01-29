from products.models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.models import *
from business_admin.models import *
from django.utils import timezone
from django.contrib.auth.models import User

class SystemLogs:

    def get_logged_in_user(request):

        """
        Retrieve the logged-in user with detailed exception handling.

        This function attempts to retrieve the currently logged-in user based on the request object.
        It handles various errors that might occur during the process, logging each error for further analysis.

        Args:
            request (Request): The request object containing the user information.

        Returns:
            tuple:
                - User or bool: The User object if the user is found, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            user, message = get_logged_in_user(request)
            if user:
                print(f"Logged in user: {user.username}")
            else:
                print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while fetching logged in user! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while fetching logged in user! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while fetching logged in user! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while fetching logged in user! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            user =  Accounts.objects.get(username = request.user)
            return user
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching logged in user! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching logged in user! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching logged in user! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while fetching logged in user! Please try again later.")
        
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
            user = SystemLogs.get_logged_in_user(request)
            if user.is_superuser and not user.is_admin:
                user_type = {
                "user_type": " Developer - Superuser",
                "username": request.user.username,
                "date": timezone.now().isoformat() 
                }
            elif user.is_staff and not user.is_admin:
                user_type = {
                "user_type": " Developer - Staff",
                "username": request.user.username,
                "date": timezone.now().isoformat() 
                }
            elif user.is_superuser and user.is_admin:
                user_type = {
                "user_type": " Admin - Superuser",
                "username": request.user.username,
                "date": timezone.now().isoformat() 
                }
            elif user.is_admin and user.is_staff:
                user_type = {
                "user_type": " Admin - Staff",
                "username": request.user.username,
                "date": timezone.now().isoformat() 
                }
            elif user.is_admin:
                user_type = {
                "user_type": " Admin",
                "username": request.user.username,
                "date": timezone.now().isoformat() 
                }
            
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

        
    def admin_activites(request,action,message=None):

        """
        Log admin activities with detailed exception handling.

        This function logs the activities performed by a business admin. It creates an entry in the `ActivityLog` model
        with the action performed and an optional message. The function includes comprehensive exception handling to log
        and report any errors that occur.

        Args:
            request (Request): The request object containing the user information.
            action (str): The action performed by the admin.
            message (str, optional): An optional message providing additional details about the action. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the activity was logged successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = admin_activites(request, action="Created a new product", message="Product ID: 123")
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating admin activities for system logs! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating admin activities for system logs! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating admin activities for system logs! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating admin activities for system logs! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            user = SystemLogs.get_logged_in_user(request)
            try:
                business_admin = BusinessAdminUser.objects.get(admin_user_name = user)
                print("ppp")
                activity = ActivityLog.objects.create(activity_done_by_admin=business_admin,action=action)
                activity.save()
                details = {
                    'action':action,
                    'message':message
                }
                current_data = activity.details or {}
                if isinstance(current_data, dict):
                    current_data.update(details)
                else:
                    current_data =details
                activity.details = current_data
                activity.save()
                return True, "Activity updated of admin"

            except:
                return False,"Business admin does not exist"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating admin activites for system logs! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating admin activites for system logs! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating admin activites for system logs! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while updating admin activites for system logs! Please try again later.")

