from .models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.models import *
from system.system_log import SystemLogs

class AdminManagement:

    #admin position
    def fetch_admin_position(pk=None,name=None):

        """
        Fetch admin positions based on various optional parameters with detailed exception handling.

        This function attempts to retrieve admin positions from the database based on the provided parameters.
        It handles various errors that might occur during the process, logging each error for further analysis.

        Args:
            pk (int, optional): The primary key (ID) of the admin position to be fetched. Defaults to None.
            name (str, optional): The name of the admin position to be fetched. Defaults to None.

        Returns:
            tuple:
                - QuerySet or AdminPositions: A QuerySet of admin positions matching the criteria or a single AdminPositions object.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            admin_position, message = fetch_admin_position(pk=1)
            print(message)

            admin_position, message = fetch_admin_position(name="Manager")
            print(message)

            admin_positions, message = fetch_admin_position()
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while fetching admin position! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while fetching admin position! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while fetching admin position! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while fetching admin position! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            if name:
                return AdminPositions.objects.get(name=name), "Admin position fetched successfully!"
            elif pk:
                return AdminPositions.objects.get(pk=pk),"Admin position fetched successfully!"
            else:
                admin_postions = AdminPositions.objects.all()
                return admin_postions,"All Admin positions fetched successfully!" if len(admin_postions)>0 else "No Admin postions found"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching admin position! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching admin position! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching admin position! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while fetching admin position! Please try again later.")

    def create_admin_position(request,name,description=None):

        """
        Create a new admin position with detailed exception handling.

        This function attempts to add a new admin position to the database. It first checks for
        existing admin positions to avoid duplicates. If the admin position does not exist, it is created.
        The function handles various errors that might occur during the process, logging each
        error for further analysis.

        Args:
            request (Request): The request object containing the user information.
            name (str): The name of the admin position to be added.
            description (str, optional): A description of the admin position. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the admin position was created successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = create_admin_position(request, name="Manager", description="Manages the team")
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating admin position! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating admin position! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating admin position! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating admin position! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """

        try:
            #getting exisitng one first
            admin_position_existing,message  = AdminManagement.fetch_admin_position()
            if any(p.name.lower() == name.lower() for p in admin_position_existing):
                return False, "Admin position with this name already exists!"
            #creating admin position
            admin_position = AdminPositions.objects.create(name=name)
            if description:
                admin_position.description = description
            admin_position.save()
            updated,message = SystemLogs.updated_by(request,admin_position)
            activity_updated, message = SystemLogs.admin_activites(request,f"Created admin position {admin_position.name}",message="created")
            return True, "Admin position created successfully"
    
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating admin position! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating admin position! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating admin position! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while creating admin position! Please try again later.")
        
    def update_admin_position(request,admin_position_pk,name,description=None):

        """
        Update an existing admin position with detailed exception handling.

        This function attempts to update the details of an admin position. It checks for changes in
        the name and description of the admin position and updates them accordingly. The function includes comprehensive
        exception handling to log and report any errors that occur.

        Args:
            request (Request): The request object containing the user information.
            admin_position_pk (int): The primary key (ID) of the admin position to be updated.
            name (str): The new name for the admin position.
            description (str, optional): The updated description of the admin position. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the admin position was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_admin_position(
                request,
                admin_position_pk=1,
                name="Senior Manager",
                description="Manages senior team"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating admin position! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating admin position! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating admin position! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating admin position! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
            if admin_position.name.lower() != name.lower():
                admin_position.name = name
            if description and admin_position.description != description.lower():
                admin_position.description = description
            admin_position.save()
            updated,message = SystemLogs.updated_by(request,admin_position)
            activity_updated, message = SystemLogs.admin_activites(request,f"Updated admin position {admin_position.name}",message="updated")
            return True, "Admin position successfully updated"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating admin position! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating admin position! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating admin position! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while updating admin position! Please try again later.")
        
    def delete_admin_position(request,admin_position_pk):

        """
        Delete an existing admin position with detailed exception handling.

        This function attempts to delete an admin position from the database. It handles various
        exceptions that might occur during the process, logging each error for further analysis.

        Args:
            request (Request): The request object containing the user information.
            admin_position_pk (int): The primary key (ID) of the admin position to be deleted.

        Returns:
            tuple:
                - bool: `True` if the admin position was deleted successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = delete_admin_position(request, admin_position_pk=1)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while deleting admin position! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while deleting admin position! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while deleting admin position! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while deleting admin position! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            #get the position
            admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
            updated,message = SystemLogs.updated_by(request,admin_position)
            activity_updated, message = SystemLogs.admin_activites(request,f"Deleted admin position {admin_position.name}",message="deleted")
            admin_position.delete()
            return True, "Admin position deleted successfully"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting admin position! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting admin position! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting admin position! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while deleting admin position! Please try again later.")
        
    #business admin users
    def fetch_business_admin_user(admin_unique_id=None):

        try:
            if admin_unique_id:
                admin_user = BusinessAdminUser.objects.get(admin_unique_id = admin_unique_id)
                return admin_user, "Business Admin user fetched successfully"
            else:
                all_admin_users = BusinessAdminUser.objects.all()
                return all_admin_users, "All Business Admin users fetched successfully" if len(all_admin_users)>0 else "No Admin users found"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching admin users! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching admin users! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching admin users! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while fetching admin users! Please try again later.")
    
    def create_business_admin_user(request,admin_full_name,admin_user_name,password,admin_position_pk,
                                   admin_contact_no=None,admin_email=None,admin_avatar=None):
        try:
            #fetching all to check if this user
            all_admins,message = AdminManagement.fetch_business_admin_user()
            if any(p.admin_user_name.lower() == admin_user_name.lower() for p in all_admins):
                return False, "Admin with this username exists"
            
            user = User.objects.create_user(username=admin_user_name,password=password)
            admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
            business_admin = BusinessAdminUser.objects.create(user=user,admin_full_name=admin_full_name,admin_user_name=admin_user_name,
                                                              admin_position = admin_position)
            business_admin.save()
            if admin_contact_no:
                business_admin.admin_contact_no = admin_contact_no
            if admin_email:
                business_admin.admin_email = admin_email
            if admin_avatar:
                business_admin.admin_avatar = admin_avatar
            business_admin.save()
            updated,message = SystemLogs.updated_by(request,business_admin)
            activity_updated, message = SystemLogs.admin_activites(request,f"Created admin {business_admin.admin_user_name}",message="Created")
            return True, "Business Admin created successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating admin user! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating admin user! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating admin user! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while creating admin user! Please try again later.")