from .models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.models import *
from system.system_log import SystemLogs
from e_commerce_app import settings
from business_admin.models import *
from system.manage_system import SystemManagement
import os
from django.db.models import Q

OWNER = 'Owner'

class AdminManagement:

    #admin position
    def fetch_admin_position(pk="",name="",available=False):

        """
        Fetch admin positions based on various optional parameters with detailed exception handling.

        This function attempts to retrieve admin positions from the database based on the provided parameters.
        If no parameter is passed, returns all admin positions.
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
            if name!="":
                return AdminPositions.objects.get(name=name), "Admin position fetched successfully!"
            elif pk!="":
                return AdminPositions.objects.get(pk=pk),"Admin position fetched successfully!"
            elif available:
                role,message = AdminManagement.fetch_admin_position(name=OWNER)
                user_role =AdminUserRole.objects.filter(role=role).exists()
                if user_role:
                    return AdminPositions.objects.all().exclude(name=OWNER),"Admin positions fetched successfully!"
                else:
                    return AdminPositions.objects.all(),"Admin positions fetched successfully!"
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

    def create_admin_position(request,name,description=""):

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
            if description != "":
                admin_position.description = description
            admin_position.save()
            SystemLogs.updated_by(request,admin_position)
            SystemLogs.admin_activites(request,f"Created admin position {admin_position.name}",message="created")
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
        
    def update_admin_position(request,admin_position_pk,name,description=""):

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
            all_admin_position,message = AdminManagement.fetch_admin_position()
            if admin_position.name.lower() != name.lower():
                for p in all_admin_position:
                    if p != admin_position and p.name.lower() == name.lower():
                        return False, "Same name already exists!"
                admin_position.name = name
            if description != "":
                admin_position.description = description
            admin_position.save()
            SystemLogs.updated_by(request,admin_position)
            SystemLogs.admin_activites(request,f"Updated admin position {admin_position.name}",message="updated")
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
            SystemLogs.admin_activites(request,f"Deleted admin position {admin_position.name}",message="deleted")
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
        
    #admin permissions
    def fetch_admin_permissions(permission_pk="",permission_name="",exclude=False):

        """
    Fetch admin permissions based on various optional parameters with detailed exception handling.

    This function attempts to retrieve admin permissions from the database based on the provided parameters.
    It handles various errors that might occur during the process, logging each error for further analysis.

    Args:
        permission_pk (str, optional): The primary key (ID) of the permission to be fetched. Defaults to an empty string.
        permission_name (str, optional): The name of the permission to be fetched. Defaults to an empty string.

    Returns:
        tuple:
            - QuerySet or AdminPermissions: A QuerySet of admin permissions if no specific permission is requested, 
              a single AdminPermissions object if a specific permission is requested by name or primary key.
            - str: A message indicating the success or failure of the operation.

    Example Usage:
        # Fetch a specific permission by name
        permission, message = fetch_admin_permissions(permission_name="view_dashboard")
        print(message)

        # Fetch a specific permission by primary key
        permission, message = fetch_admin_permissions(permission_pk=1)
        print(message)

        # Fetch all permissions
        all_permissions, message = fetch_admin_permissions()
        print(message)

    Exception Handling:
        - **DatabaseError**: Catches general database-related issues.
            Message: "An unexpected error in Database occurred while fetching admin permissions! Please try again later."
        - **OperationalError**: Handles server-related issues such as connection problems.
            Message: "An unexpected error in server occurred while fetching admin permissions! Please try again later."
        - **ProgrammingError**: Catches programming errors such as invalid queries.
            Message: "An unexpected error in server occurred while fetching admin permissions! Please try again later."
        - **IntegrityError**: Handles data integrity issues.
            Message: "Same type exists in Database!"
        - **Exception**: A catch-all for any other unexpected errors.
            Message: "An unexpected error occurred while fetching admin permissions! Please try again later."

    Notes:
        - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
    """
        try:
            if permission_name!="":
                permission_name = permission_name.lower()
                permission =  AdminPermissions.objects.get(permission_name = permission_name)
                return permission, "Permission fetched successfully"
            elif permission_pk!="":
                permission =  AdminPermissions.objects.get(pk=permission_pk)
                return permission,"Permission fetched successfully"
            elif exclude:
                permission = AdminPermissions.objects.exclude(Q(permission_name="view") | Q(permission_name="change"))
                return permission,"All permissions fetched successfully" if len(permission)>0 else "No permissions found"
            else:
                permission = AdminPermissions.objects.filter(Q(permission_name="view") | Q(permission_name="change"))
                return permission, "All permissions fetched successfully" if len(permission)>0 else "No permissions found"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching admin permissions! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching admin permissions! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching admin permissions! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while fetching admin permissions! Please try again later.")
        
    def create_admin_permissions(request,permission_name,permission_description=""):

        """
    Create a new admin permission with detailed exception handling.

    This function attempts to add a new admin permission to the database. It first checks if a permission with the same name
    already exists. If it does, it returns an error message. Otherwise, it creates a new permission with the specified name
    and optional description. The function handles various errors that might occur during the process, logging each error for
    further analysis.

    Args:
        request (Request): The request object containing the user information.
        permission_name (str): The name of the permission to be created.
        permission_description (str, optional): The description of the permission. Defaults to an empty string.

    Returns:
        tuple:
            - bool: `True` if the permission was created successfully, `False` otherwise.
            - str: A message indicating the success or failure of the operation.

    Example Usage:
        success, message = create_admin_permissions(
            request,
            permission_name="view_dashboard",
            permission_description="Permission to view the dashboard"
        )
        print(message)

    Exception Handling:
        - **DatabaseError**: Catches general database-related issues.
            Message: "An unexpected error in Database occurred while creating admin permissions! Please try again later."
        - **OperationalError**: Handles server-related issues such as connection problems.
            Message: "An unexpected error in server occurred while creating admin permissions! Please try again later."
        - **ProgrammingError**: Catches programming errors such as invalid queries.
            Message: "An unexpected error in server occurred while creating admin permissions! Please try again later."
        - **IntegrityError**: Handles data integrity issues.
            Message: "Same type exists in Database!"
        - **Exception**: A catch-all for any other unexpected errors.
            Message: "An unexpected error occurred while creating admin permissions! Please try again later."

    Notes:
        - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
    """
        
        try:
            #exisitng permissions
            permission_name = permission_name.lower()
            all_permissions,message = AdminManagement.fetch_admin_permissions()
            for p in all_permissions:
                if p.permission_name.lower() == permission_name:
                    return False, "Admin permission with this name already exists"
            
            if permission_name == AdminPermissions.CREATE:
                permission = AdminPermissions.objects.create(permission_name=AdminPermissions.CREATE)
            elif permission_name == AdminPermissions.UPDATE:
                permission = AdminPermissions.objects.create(permission_name=AdminPermissions.UPDATE)
            elif permission_name == AdminPermissions.VIEW:
                permission = AdminPermissions.objects.create(permission_name=AdminPermissions.VIEW)
            elif permission_name == AdminPermissions.DELETE:
                permission = AdminPermissions.objects.create(permission_name=AdminPermissions.DELETE)
            
            permission.save()
            if permission_description !="":
                permission.permission_description = permission_description
            permission.save()
            SystemLogs.updated_by(request,permission)
            SystemLogs.admin_activites(request,f"Created admin permissions {permission.permission_name}",message="Created")
            return True, "Admin permission created successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating admin permissions! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating admin permissions! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating admin permissions! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while creating admin permissions! Please try again later.")
        
    def update_admin_permissions(request,admin_permission_pk,permission_name,permission_description=""):
        
        """
        Update an existing admin permission with detailed exception handling.

        This function attempts to update an existing admin permission in the database. It fetches the permission
        using the provided primary key (admin_permission_pk) and updates its attributes with the specified values.
        The function handles various errors that might occur during the process, logging each error for further analysis.

        Args:
            request (Request): The request object containing the user information.
            admin_permission_pk (int): The primary key (ID) of the admin permission to be updated.
            permission_name (str): The new name of the permission.
            permission_description (str, optional): The new description of the permission. Defaults to an empty string.

        Returns:
            tuple:
                - bool: `True` if the permission was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_admin_permissions(
                request,
                admin_permission_pk=1,
                permission_name="edit_dashboard",
                permission_description="Permission to edit the dashboard"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating admin permissions! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating admin permissions! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating admin permissions! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating admin permissions! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            #getting permission
            admin_permission,message = AdminManagement.fetch_admin_permissions(permission_pk=admin_permission_pk)
            all_permissions,message = AdminManagement.fetch_admin_permissions()
            for p in all_permissions:
                if p!=admin_permission and p.permission_name.lower() == permission_name.lower():
                    return False, "Permission with this name already exists"
            if admin_permission.permission_name != permission_name.lower():
                admin_permission.permission_name = permission_name
            if permission_description!="":
                admin_permission.permission_description = permission_description
            admin_permission.save()
            SystemLogs.updated_by(request,admin_permission)
            SystemLogs.admin_activites(request,f"Updated admin permissions {admin_permission.permission_name}",message="Updated")
            return True, "Admin permissions updated successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating admin permissions! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating admin permissions! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating admin permissions! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while updating admin permissions! Please try again later.")
    
    def delete_admin_permissions(request,admin_permission_pk):

        """
    Delete an existing admin permission with detailed exception handling.

    This function attempts to delete an existing admin permission from the database. It fetches the permission
    using the provided primary key (admin_permission_pk) and deletes it. The function handles various errors that
    might occur during the process, logging each error for further analysis.

    Args:
        request (Request): The request object containing the user information.
        admin_permission_pk (int): The primary key (ID) of the admin permission to be deleted.

    Returns:
        tuple:
            - bool: `True` if the permission was deleted successfully, `False` otherwise.
            - str: A message indicating the success or failure of the operation.

    Example Usage:
        success, message = delete_admin_permissions(
            request,
            admin_permission_pk=1
        )
        print(message)

    Exception Handling:
        - **DatabaseError**: Catches general database-related issues.
            Message: "An unexpected error in Database occurred while deleting admin permissions! Please try again later."
        - **OperationalError**: Handles server-related issues such as connection problems.
            Message: "An unexpected error in server occurred while deleting admin permissions! Please try again later."
        - **ProgrammingError**: Catches programming errors such as invalid queries.
            Message: "An unexpected error in server occurred while deleting admin permissions! Please try again later."
        - **IntegrityError**: Handles data integrity issues.
            Message: "Same type exists in Database!"
        - **Exception**: A catch-all for any other unexpected errors.
            Message: "An unexpected error occurred while deleting admin permissions! Please try again later."

    Notes:
        - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
    """

        try:
            #getting the perimission
            admin_permission,message = AdminManagement.fetch_admin_permissions(permission_pk=admin_permission_pk)
            admin_permission.delete()
            SystemLogs.admin_activites(request,f"Deleted admin permissions {admin_permission.permission_name}",message="Deleted")
            return True, "Admin permission deleted successfully"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting admin permissions! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting admin permissions! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting admin permissions! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while deleting admin permissions! Please try again later.")
    
    #business admin users
    def fetch_business_admin_user(admin_unique_id="",admin_email="",admin_user_name=""):

        """
        Fetch business admin users based on various optional parameters
        admin_unique_id or admin_user_name, with detailed exception handling.
        With no parameters returns all business admin user
        This function attempts to retrieve business admin users from the database based on the provided parameters.
        It handles various errors that might occur during the process, logging each error for further analysis.

        Args:
            admin_unique_id (str, optional): The unique ID of the admin to be fetched. Defaults to None.
            admin_user_name (str, optional): The username of the admin to be fetched. Defaults to None.

        Returns:
            tuple:
                - BusinessAdminUser or QuerySet: A single BusinessAdminUser object or a QuerySet of business admin users matching the criteria.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            admin_user, message = fetch_business_admin_user(admin_unique_id="12345")
            print(message)

            admin_user, message = fetch_business_admin_user(admin_user_name="admin")
            print(message)

            admin_users, message = fetch_business_admin_user()
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while fetching admin users! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while fetching admin users! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while fetching admin users! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while fetching admin users! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """

        try:
            if admin_unique_id!="":
                admin_user = BusinessAdminUser.objects.get(admin_unique_id = admin_unique_id)
                return admin_user, "Business Admin user fetched successfully"
            elif admin_email!="":
                admin_user = BusinessAdminUser.objects.get(admin_email=admin_email)
                return admin_user, "Business Admin user fetched successfully"
            elif admin_user_name!="":
                admin_user = BusinessAdminUser.objects.get(admin_user_name=admin_user_name)
                return admin_user,"Business Admin user fetched successfully"
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
    
    def create_business_admin_user(admin_full_name,password,
                                   admin_email,admin_contact_no="",admin_avatar="",is_superuser=False,is_staff_user=False):
    
        """
        Create a new business admin user with detailed exception handling.

        This function attempts to add a new business admin user to the database. It first checks for
        existing admin users to avoid duplicates. If the admin user does not exist, it is created.
        The function handles various errors that might occur during the process, logging each
        error for further analysis.

        Args:
            admin_full_name (str): The full name of the admin user to be added.
            password (str): The password for the admin user.
            admin_email (str, optional): The email address of the admin user.
            admin_contact_no (str, optional): The contact number of the admin user. Defaults to None.
            admin_avatar (str, optional): The avatar image of the admin user. Defaults to None.
            is_staff_user = False default
            is_superuser = False default

        Returns:
            tuple:
                - bool: `True` if the admin user was created successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = create_business_admin_user(
                admin_full_name="John Doe",
                password="securepassword",
                admin_contact_no="1234567890",
                admin_email="johndoe@example.com",
                admin_avatar="path/to/avatar.jpg"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating admin user! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating admin user! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating admin user! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating admin user! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """

        SUBJECT = "Admin Account Created"
        BODY = "Welcome Admin, ....."

        try:
            #fetching all to check if this user
            all_admins,message = AdminManagement.fetch_business_admin_user()
            if any(p.admin_email == admin_email for p in all_admins):
                return False, "Admin with this email already exists"
            admin_user_name = admin_email.split('@')[0]
            count_admin_user_name = 0
            for p in all_admins:
                if p.admin_user_name.lower() == admin_user_name.lower():
                    count_admin_user_name += 1
            if count_admin_user_name == 0:
                admin_user_name = admin_user_name
            else:
                admin_user_name = admin_user_name + str(count_admin_user_name)

            business_admin = BusinessAdminUser.objects.create(admin_full_name=admin_full_name,admin_user_name=admin_user_name,
                                                              )
            business_admin.save()
            #creating admin account
            new_business_admin_user = Accounts(email = admin_email,username = admin_user_name,is_admin=True)
            new_business_admin_user.set_password(password)
            new_business_admin_user.save()

            if is_staff_user:
                new_business_admin_user.is_staff = True
            if is_superuser:
                new_business_admin_user.is_superuser = True
            new_business_admin_user.save()

            if admin_contact_no != "":
                business_admin.admin_contact_no = admin_contact_no
            if admin_email != "":
                business_admin.admin_email = admin_email
            if admin_avatar != "":
                business_admin.admin_avatar = admin_avatar
            business_admin.save()
            SystemManagement.send_email(subject=SUBJECT,body=BODY,emails_to=[admin_email])
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

    def update_business_admin_user(request,admin_username,admin_full_name="",admin_email="",
                                   admin_contact_no="",admin_avatar="",old_password="",
                                   password="",is_superuser=False,is_staff_user=False):
        
        """
        Update an existing business admin user with detailed exception handling.

        This function attempts to update the details of a business admin user. It checks for changes in
        the full name, position, contact number, email, avatar, and password of the admin user and updates them accordingly.
        The function includes comprehensive exception handling to log and report any errors that occur.

        Args:
            request (Request): The request object containing the user information.
            admin_unique_id (str): The unique ID of the admin user to be updated.
            admin_full_name (str): The new full name for the admin user.
            admin_contact_no (str, optional): The updated contact number of the admin user. Defaults to None.
            admin_email (str, optional): The updated email address of the admin user. Defaults to None.
            admin_avatar (str, optional): The updated avatar image of the admin user. Defaults to None.
            old_password (str, optional): The old password of the admin user for verification. Defaults to None.
            password (str, optional): The new password for the admin user. Defaults to None.
            is_superuser: False default
            is_staff_user: False default

        Returns:
            tuple:
                - bool: `True` if the admin user was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_business_admin_user(
                request,
                admin_unique_id="12345",
                admin_full_name="John Doe",
                admin_contact_no="1234567890",
                admin_email="johndoe@example.com",
                admin_avatar="path/to/avatar.jpg",
                old_password="oldpassword",
                password="newpassword"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating admin user! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating admin user! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating admin user! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating admin user! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            #getting the admin user
            business_admin_user,message = AdminManagement.fetch_business_admin_user(admin_user_name=admin_username)
            all_business_admin_user,message = AdminManagement.fetch_business_admin_user()
            user = Accounts.objects.get(username=business_admin_user.admin_user_name)
            if user.is_staff == False and is_staff_user == True:
                user.is_staff = True
            if user.is_superuser == False and is_superuser == True:
                user.is_superuser = True
            user.save()
            #checking conditions to update as necessarily
            if password:
                if user.check_password(old_password):
                    user.set_password(password)
                    user.save()
                else:
                    return False, "Old password is incorrect"
            if admin_full_name!="" and business_admin_user.admin_full_name.lower() != admin_full_name.lower():
                business_admin_user.admin_full_name = admin_full_name
            if admin_contact_no!="":
                business_admin_user.admin_contact_no = admin_contact_no
            if admin_email!="" and business_admin_user.admin_email != admin_email:
                for p in all_business_admin_user:
                    if p != business_admin_user and p.admin_email == admin_email:
                        return False, "This email is already taken"
                business_admin_user.admin_email = admin_email
                user.email = admin_email
            if admin_avatar != "":
                if business_admin_user.admin_avatar:
                    path = settings.MEDIA_ROOT+str(business_admin_user.admin_avatar)
                    if os.path.exists(path):
                        os.remove(path)
                    business_admin_user.admin_avatar.delete()
                business_admin_user.admin_avatar = admin_avatar
            business_admin_user.save()
            user.save()
            SystemLogs.updated_by(request,business_admin_user)
            SystemLogs.admin_activites(request,f"Updated admin {business_admin_user.admin_user_name}",message="Updated")
            return True, "Business Admin successfully updated"
            
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating admin user! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating admin user! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating admin user! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while updating admin user! Please try again later.")
        
    def update_business_admin_user_password(request,admin_user_name,old_password,new_password):

        """
        Update the password of an existing business admin user with detailed exception handling.

        This function attempts to update the password of a business admin user. It verifies the old password
        before setting the new password. The function includes comprehensive exception handling to log and report any errors that occur.

        Args:
            request (Request): The request object containing the user information.
            admin_unique_id (str): The unique ID of the admin user whose password is to be updated.
            old_password (str): The old password of the admin user for verification.
            new_password (str): The new password for the admin user.

        Returns:
            tuple:
                - bool: `True` if the password was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_business_admin_user_password(
                request,
                admin_unique_id="12345",
                old_password="oldpassword",
                new_password="newpassword"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating admin password! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating admin password! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating admin password! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating admin password! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            business_admin_user,message = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)
            user = Accounts.objects.get(username = business_admin_user.admin_user_name)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
            else:
                return False, "Old password is incorrect"
            SystemLogs.updated_by(request,business_admin_user)
            SystemLogs.admin_activites(request,f"Updated admin password {business_admin_user.admin_user_name}",message="Updated password")
            return True, "Password updated successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating admin password! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating admin password! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating admin password! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while updating admin password! Please try again later.")
    
    def reset_business_admin_user_password(request,admin_email,new_password):

        """
        Reset the password of an existing business admin user with detailed exception handling.

        This function attempts to reset the password of a business admin user. It sets the new password
        without requiring the old password. The function includes comprehensive exception handling to log and report any errors that occur.

        Args:
            request (Request): The request object containing the user information.
            admin_user_name (str): The username of the admin user whose password is to be reset.
            new_password (str): The new password for the admin user.

        Returns:
            tuple:
                - bool: `True` if the password was reset successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = reset_business_admin_user_password(
                request,
                admin_user_name="admin",
                new_password="newpassword"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while resetting admin password! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while resetting admin password! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while resetting admin password! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while resetting admin password! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """

        try:

            #fetching the Business Admin user using user name
            business_admin_user,message = AdminManagement.fetch_business_admin_user(admin_email=admin_email)
            user = Accounts.objects.get(username = business_admin_user.admin_user_name)
            user.set_password(new_password)
            user.save()
            SystemLogs.updated_by(request,business_admin_user)
            SystemLogs.admin_activites(request,f"Reset admin password {business_admin_user.admin_user_name}",message="Reset password")
            return True, "Password reset successfull"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while resetting admin password! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while resetting admin password! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while resetting admin password! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while resetting admin password! Please try again later.")
        
    def delete_business_admin_user(request,admin_unique_id):

        """
        Delete an existing business admin user with detailed exception handling.

        This function attempts to delete a business admin user from the database. It handles various
        exceptions that might occur during the process, logging each error for further analysis.

        Args:
            request (Request): The request object containing the user information.
            admin_unique_id (str): The unique ID of the admin user to be deleted.

        Returns:
            tuple:
                - bool: `True` if the admin user was deleted successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = delete_business_admin_user(request, admin_unique_id="12345")
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while deleting admin user! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while deleting admin user! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while deleting admin user! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while deleting admin user! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            #getting the admin
            business_admin_user,message = AdminManagement.fetch_business_admin_user(admin_unique_id=admin_unique_id)
            user = Accounts.objects.get(username = business_admin_user.admin_user_name)
            if business_admin_user.admin_avatar:
                path = settings.MEDIA_ROOT+str(business_admin_user.admin_avatar)
                if os.path.exists(path):
                    os.remove(path)
                business_admin_user.admin_avatar.delete()
            SystemLogs.admin_activites(request,f"Deleted admin {business_admin_user.admin_user_name}",message="Deleted")
            business_admin_user.delete()
            user.delete()
            return True, "Admin deleted successfully"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting admin user! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting admin user! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting admin user! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while deleting admin user! Please try again later.")
        
    def fetch_postion_of_admin(request,admin_user_name):

        """
    Fetch the position of an admin user with detailed exception handling.

    This function attempts to retrieve the position of an admin user from the database based on the provided admin username.
    It handles various errors that might occur during the process, logging each error for further analysis.

    Args:
        request (Request): The request object containing the user information.
        admin_user_name (str): The username of the admin whose position is to be fetched.

    Returns:
        tuple:
            - AdminPosition or bool: The position of the admin user if it exists, otherwise `False`.
            - str: A message indicating the success or failure of the operation.

    Example Usage:
        position, message = fetch_postion_of_admin(request, admin_user_name="admin_user")
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
            #getting the admin
            business_admin,message = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)
            if business_admin.admin_position:
                return business_admin.admin_position, "Fetched successfully"
            else:
                return False, "No position yet"

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
    
    def fetch_extra_postions_of_admin(admin_user_name):

        try:
            #sall_permissions,message = AdminManagement.fetch_admin_permissions(exclude=True)
            user = Accounts.objects.get(username = admin_user_name)
            try:
                admin_user_role = AdminUserRole.objects.get(user = user)
                extra_permissions = admin_user_role.extra_permissions.all()
            except:
                extra_permissions = []
            
            return extra_permissions, "Fetched Successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching admin extra position! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching admin extra position! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching admin extra position! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while fetching admin extra position! Please try again later.")
        
    def add_user_admin_position(request,admin_user_name,admin_position_pk,extra_permissions_pk_list=[]):

        """
    Assigns an admin position to a user and creates an admin role entry.

    Parameters:
    ----------
    request : HttpRequest
        The request object, used for logging system activities.
    admin_user_name : str
        The username of the admin to whom the position should be assigned.
    admin_position_pk : str
        The primary key of the admin position to be assigned.

    Returns:
    -------
    tuple (bool, str)
        - If the assignment is successful: (True, "Successfully added")
        - If the user already has a role: (False, "Admin already has a role")
        - If an error occurs: (False, <error_message>)

    Raises:
    ------
    Handles and logs the following exceptions:
        - DatabaseError: Raised for unexpected database errors.
        - OperationalError: Raised for unexpected server errors.
        - ProgrammingError: Raised for programming-related errors.
        - IntegrityError: Raised for database integrity constraint violations.
        - Exception: Catches any other unexpected errors.

    Process:
    -------
    1. Fetches the user with `admin_user_name` from the `Accounts` model.
    2. Checks if the user already has an admin role; if so, returns an error.
    3. Fetches the business admin record and the admin position using `AdminManagement`.
    4. Assigns the admin position to the business admin and saves it.
    5. Logs the activity using `SystemLogs`.
    6. Creates a new `AdminUserRole` entry linking the user to the admin position.
    7. Logs the user role assignment activity.
    8. Returns success or handles errors if encountered.

    Error Handling:
    --------------
    - Logs errors in the `ErrorLogs` model with the error type and message.
    - Returns appropriate user-friendly error messages based on the exception type.

    Example Usage:
    -------------
    >>> add_user_admin_position(request, "john_doe", "5")
    (True, "Successfully added")

    >>> add_user_admin_position(request, "admin_user", "2")
    (False, "Admin already has a role")

    >>> add_user_admin_position(request, "invalid_user", "3")
    (False, "An unexpected error in Database occurred while adding admin position! Please try again later.")
    """

        try:
            #getting the admin
            user = Accounts.objects.get(username = admin_user_name)
            all_exisiting_user_role = AdminUserRole.objects.filter(user = user)
            if all_exisiting_user_role.first():
                return False, "Admin already has a role"
            
            business_admin,message = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)
            admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
            business_admin.admin_position = admin_position
            business_admin.save()
            SystemLogs.updated_by(request,business_admin)
            SystemLogs.admin_activites(request,f"Admin position added, {business_admin.admin_user_name}",message="Admin position added")

            admin_user_role = AdminUserRole.objects.create(user = user,role = admin_position)
            admin_user_role.save()
            if len(extra_permissions_pk_list)>0:
                permissions_list = []
                for p in extra_permissions_pk_list:
                    permission,message = AdminManagement.fetch_admin_permissions(permission_pk=p)
                    permissions_list.append(permission)
                admin_user_role.extra_permissions.add(*permissions_list)
                admin_user_role.save()

            SystemLogs.updated_by(request,admin_user_role)
            SystemLogs.admin_activites(request,f"Admin user role added, {admin_user_role.user.username}",message="Admin user role added")

            return True, "Successfully added"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while adding admin position! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while adding admin position! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while adding admin position! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while adding admin position! Please try again later.")
    
    def update_user_admin_position(request,admin_user_name,admin_position_pk="",extra_permissions_pk_list=[]):

        """
    Updates or removes an admin user's assigned position.

    Parameters:
    ----------
    request : HttpRequest
        The request object, used for logging system activities.
    admin_user_name : str
        The username of the admin whose position needs to be updated.
    admin_position_pk : str, optional
        The primary key of the new admin position. If empty (""), the admin position will be removed.

    Returns:
    -------
    tuple (bool, str)
        - If the update is successful: (True, "Successfully updated")
        - If an error occurs: (False, <error_message>)

    Raises:
    ------
    Handles and logs the following exceptions:
        - DatabaseError: Raised for unexpected database errors.
        - OperationalError: Raised for unexpected server errors.
        - ProgrammingError: Raised for programming-related errors.
        - IntegrityError: Raised for database integrity constraint violations.
        - Exception: Catches any other unexpected errors.

    Process:
    -------
    1. Fetches the user with `admin_user_name` from the `Accounts` model.
    2. Retrieves the corresponding `AdminUserRole` and `business_admin` details.
    3. If `admin_position_pk` is empty (""), the admin's role is removed:
        - Sets `admin_user_role.role` to `None` and saves it.
        - Logs the removal using `SystemLogs`.
        - Updates `business_admin.admin_position` to `None` and saves it.
    4. If a new position is provided and differs from the existing one:
        - Fetches the `AdminPosition` using `AdminManagement`.
        - Updates `admin_user_role.role` and `business_admin.admin_position`.
        - Logs the updates using `SystemLogs`.
    5. Returns success or handles errors if encountered.

    Error Handling:
    --------------
    - Logs errors in the `ErrorLogs` model with the error type and message.
    - Returns appropriate user-friendly error messages based on the exception type.

    Example Usage:
    -------------
    >>> update_user_admin_position(request, "john_doe", "5")
    (True, "Successfully updated")

    >>> update_user_admin_position(request, "admin_user")
    (True, "Successfully updated")  # Removes the admin position

    >>> update_user_admin_position(request, "invalid_user", "3")
    (False, "An unexpected error in Database occurred while updating admin position! Please try again later.")
    """

        try:
            #getting the admin
            user = Accounts.objects.get(username = admin_user_name)
            admin_user_role = AdminUserRole.objects.get(user = user)
            business_admin,message = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)

            if admin_position_pk == "":
                admin_user_role.role = None
                admin_user_role.save()
                SystemLogs.updated_by(request,admin_user_role)
                SystemLogs.admin_activites(request,f"Admin user role removed, {admin_user_role.user.username}",message="Admin user role removed")
                business_admin.admin_position = None
                business_admin.save()
                SystemLogs.updated_by(request,business_admin)
                SystemLogs.admin_activites(request,f"Admin position removed, {business_admin.admin_user_name}",message="Admin position removed") 

            elif business_admin.admin_position.pk != admin_position_pk:
                admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
                admin_user_role.role = admin_position
                admin_user_role.save()
                SystemLogs.updated_by(request,admin_user_role)
                SystemLogs.admin_activites(request,f"Admin user role updated, {admin_user_role.user.username}",message="Admin user role updated")
                business_admin.admin_position = admin_position
                business_admin.save()
                SystemLogs.updated_by(request,business_admin)
                SystemLogs.admin_activites(request,f"Admin position updated, {business_admin.admin_user_name}",message="Admin position updated")
            
            elif len(extra_permissions_pk_list)>0:
                new_extra_permissions = []
                for p in extra_permissions_pk_list:
                    permission,message = AdminManagement.fetch_admin_permissions(permission_pk=p)
                    new_extra_permissions.append(permission)
                admin_user_role.extra_permissions.clear()
                admin_user_role.extra_permissions.add(*new_extra_permissions)
                admin_user_role.save()

            return True, "Successfully updated"

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
    
    def remove_position_of_admin(request,admin_user_name,delete=False):

        """
    Remove the position of an admin user with detailed exception handling.

    This function attempts to remove the position of an admin user in the database. It fetches the admin user
    using the provided username and sets the admin user's position to `None`. The function handles various errors
    that might occur during the process, logging each error for further analysis.

    Args:
        request (Request): The request object containing the user information.
        admin_user_name (str): The username of the admin whose position is to be removed.
        delete (bool, optional): A flag indicating whether to delete the admin user role. Defaults to False.

    Returns:
        tuple:
            - bool: `True` if the admin position was removed successfully, `False` otherwise.
            - str: A message indicating the success or failure of the operation.
            - bool: `True` if the admin user role was deleted successfully, `False` otherwise.

    Example Usage:
        success, message = remove_position_of_admin(
            request,
            admin_user_name="admin_user",
            delete=True
        )
        print(message)

    Exception Handling:
        - **DatabaseError**: Catches general database-related issues.
            Message: "An unexpected error in Database occurred while removing admin position! Please try again later."
        - **OperationalError**: Handles server-related issues such as connection problems.
            Message: "An unexpected error in server occurred while removing admin position! Please try again later."
        - **ProgrammingError**: Catches programming errors such as invalid queries.
            Message: "An unexpected error in server occurred while removing admin position! Please try again later."
        - **IntegrityError**: Handles data integrity issues.
            Message: "Same type exists in Database!"
        - **Exception**: A catch-all for any other unexpected errors.
            Message: "An unexpected error occurred while removing admin position! Please try again later."

    Notes:
        - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
    """

        try:
            #getting the admin
            user = Accounts.objects.get(username = admin_user_name)
            admin_user_role = AdminUserRole.objects.get(user = user)
            admin_user_role.role = None
            admin_user_role.extra_permissions.clear()
            admin_user_role.save()
            SystemLogs.updated_by(request,admin_user_role)
            SystemLogs.admin_activites(request,f"Admin user role removed, {admin_user_role.user.username}",message="Admin user role removed")
            business_admin,message = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)
            business_admin.admin_position = None
            business_admin.save()
            SystemLogs.updated_by(request,business_admin)
            SystemLogs.admin_activites(request,f"Admin position removed, {business_admin.admin_user_name}",message="Admin position removed")
            if delete:
                admin_user_role.delete()
            return True, "Admin position removed successfully"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while removing admin position! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while removing admin position! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while removing admin position! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while removing admin position! Please try again later.")
        
    def fetch_business_admin_profile_picture(admin_unique_id="",admin_email="",admin_user_name=""):

        """
    Fetches the profile picture (avatar) of a business administrator using one of the provided identifiers.

    Parameters:
    ----------
    admin_unique_id : str, optional
        The unique identifier of the business admin. Default is an empty string.
    admin_email : str, optional
        The email of the business admin. Default is an empty string.
    admin_user_name : str, optional
        The username of the business admin. Default is an empty string.

    Returns:
    -------
    tuple (bool | str, str)
        - If an avatar is found: (avatar_url: str, "Avatar fetched successfully")
        - If no avatar is found: (False, "No avatar found")
        - If an error occurs: (False, <error_message>)

    Raises:
    ------
    Handles and logs the following exceptions:
        - DatabaseError: Raised for unexpected database errors.
        - OperationalError: Raised for unexpected server errors.
        - ProgrammingError: Raised for programming-related errors.
        - IntegrityError: Raised for database integrity constraint violations.
        - Exception: Catches any other unexpected errors.

    Error Handling:
    --------------
    - Logs errors in the `ErrorLogs` model with the error type and message.
    - Returns appropriate user-friendly error messages based on the exception type.

    Example Usage:
    -------------
    >>> fetch_business_admin_profile_picture(admin_email="admin@example.com")
    ("https://example.com/admin_avatar.jpg", "Avatar fetched successfully")

    >>> fetch_business_admin_profile_picture(admin_email="nonexistent@example.com")
    (False, "No avatar found")

    >>> fetch_business_admin_profile_picture(admin_unique_id="invalid_id")
    (False, "An unexpected error in Database occurred while fetching admin avatar! Please try again later.")
    """
        
        try:
            if admin_unique_id!="":
                business_admin,message = AdminManagement.fetch_business_admin_user(admin_unique_id=admin_unique_id)
            elif admin_email!="":
                business_admin,message = AdminManagement.fetch_business_admin_user(admin_email=admin_email)
            elif admin_user_name!="":
                business_admin,message = AdminManagement.fetch_business_admin_user(admin_user_name=admin_user_name)
            
            if business_admin.admin_avatar:
                avatar_url = business_admin.admin_avatar
                return avatar_url, "Avatar fetched successfully"
            else:
                return False, "No avatar found"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching admin avatar! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching admin avatar! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching admin avatar! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while removing admin position! Please try again later.")
        
    #admin role permissions
    def fetch_admin_role_permission(admin_role_permission_pk="",admin_position_pk="",admin_permission_pk=""):

        """
    Fetches admin role permissions based on the provided identifiers.

    Parameters:
    ----------
    admin_role_permission_pk : str, optional
        The primary key of the admin role permission. Default is an empty string.
    admin_position_pk : str, optional
        The primary key of the admin position. Default is an empty string.
    admin_permission_pk : str, optional
        The primary key of the admin permission. Default is an empty string.

    Returns:
    -------
    tuple (QuerySet | object | bool, str)
        - If an admin role permission is found: (admin_role_permission: QuerySet | object, "Fetched successfully")
        - If no matching role permissions exist: (False, "No role and permissions found")
        - If an error occurs: (False, <error_message>)

    Raises:
    ------
    Handles and logs the following exceptions:
        - DatabaseError: Raised for unexpected database errors.
        - OperationalError: Raised for unexpected server errors.
        - ProgrammingError: Raised for programming-related errors.
        - IntegrityError: Raised for database integrity constraint violations.
        - Exception: Catches any other unexpected errors.

    Error Handling:
    --------------
    - Logs errors in the `ErrorLogs` model with the error type and message.
    - Returns appropriate user-friendly error messages based on the exception type.

    Example Usage:
    -------------
    >>> fetch_admin_role_permission(admin_role_permission_pk="123")
    (<AdminRolePermission object>, "Fetched successfully")

    >>> fetch_admin_role_permission(admin_position_pk="10")
    (<QuerySet of AdminRolePermission objects>, "Fetched successfully")

    >>> fetch_admin_role_permission(admin_permission_pk="50")
    (<QuerySet of AdminRolePermission objects>, "Fetched successfully")

    >>> fetch_admin_role_permission(admin_position_pk="invalid")
    (False, "No role and permissions found")

    >>> fetch_admin_role_permission()
    (<QuerySet of all AdminRolePermission objects>, "All fetched successfully")
    """

        try:
            if admin_role_permission_pk!="":
                admin_role_permission = AdminRolePermission.objects.get(pk=admin_role_permission_pk)
                return admin_role_permission, "Fetched successfully"
            elif admin_position_pk!="":
                admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
                admin_role_permission = AdminRolePermission.objects.filter(role=admin_position)
                return admin_role_permission, "Fetched successfully" if len(admin_role_permission)>0 else "No role and permissions found"
            elif admin_permission_pk!="":
                admin_permission,message = AdminManagement.fetch_admin_permissions(permission_pk=admin_permission_pk)
                admin_role_permission = AdminRolePermission.objects.filter(permission=admin_permission)
                return admin_role_permission, "Fetched successfully" if len(admin_role_permission)>0 else "No role and permissions found"
            else:
                admin_role_permission = AdminRolePermission.objects.all()
                return admin_role_permission, "All fetched successfully" if len(admin_role_permission)>0 else "No role and permissions found"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching admin role permission! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching admin role permission! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching admin role permission! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while fetching admin role permission! Please try again later.")
        
    def create_admin_role_permission(request,admin_position_pk,admin_permission_pk_list):

        """
    Creates admin role permissions by associating an admin position with a list of permissions.

    Parameters:
    ----------
    request : HttpRequest
        The request object, used for logging system activities.
    admin_position_pk : str
        The primary key of the admin position for which permissions need to be assigned.
    admin_permission_pk_list : list
        A list of permission primary keys to be assigned to the admin position.

    Returns:
    -------
    tuple (bool, str)
        - If new permissions are created: (True, "Created successfully")
        - If all provided permissions already exist: (True, "Already exists")
        - If an error occurs: (False, <error_message>)

    Raises:
    ------
    Handles and logs the following exceptions:
        - DatabaseError: Raised for unexpected database errors.
        - OperationalError: Raised for unexpected server errors.
        - ProgrammingError: Raised for programming-related errors.
        - IntegrityError: Raised for database integrity constraint violations.
        - Exception: Catches any other unexpected errors.

    Process:
    -------
    1. Fetches the admin position using `admin_position_pk`.
    2. Retrieves all existing role permissions.
    3. Filters out permissions that are already assigned to the admin position.
    4. Creates new role permissions for the remaining ones.
    5. Logs the creation process using `SystemLogs`.

    Error Handling:
    --------------
    - Logs errors in the `ErrorLogs` model with the error type and message.
    - Returns appropriate user-friendly error messages based on the exception type.

    Example Usage:
    -------------
    >>> create_admin_role_permission(request, "10", ["101", "102"])
    (True, "Created successfully")

    >>> create_admin_role_permission(request, "10", ["101"])
    (True, "Already exists")

    >>> create_admin_role_permission(request, "invalid", ["101"])
    (False, "An unexpected error in Database occurred while creating admin role permission! Please try again later.")
    """

        try:
        
            #getting admin_position
            admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
            all_existing_admin_role_permissions,message = AdminManagement.fetch_admin_role_permission()
            admin_permission_pk_list_copy = admin_permission_pk_list.copy()
            for admin_permission_pk in admin_permission_pk_list_copy:
                admin_permission,message = AdminManagement.fetch_admin_permissions(permission_pk=admin_permission_pk)
                #checking if exisitng permission for this admin position exists. If do removing it
                if any(p.role == admin_position and p.permission == admin_permission for p in all_existing_admin_role_permissions):
                    admin_permission_pk_list.remove(admin_permission_pk)
            for admin_permission_pk in admin_permission_pk_list:
                admin_permission,message = AdminManagement.fetch_admin_permissions(permission_pk=admin_permission_pk)
                admin_role_permissions = AdminRolePermission.objects.create(role=admin_position,permission=admin_permission)
                admin_role_permissions.save()
                SystemLogs.updated_by(request,admin_role_permissions)
                SystemLogs.admin_activites(request,f"Created admin role permission {admin_role_permissions.role.name}",message="Created")
            return True, "Created successfully" if len(admin_permission_pk_list)>0 else "Already exists"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating admin role permission! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating admin role permission! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating admin role permission! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while creating admin role permission! Please try again later.")
        
    def update_admin_role_permission(request,admin_position_pk="",admin_permission_pk_list=[]):

        """
    Updates admin role permissions by replacing existing permissions with a new set.

    Parameters:
    ----------
    request : HttpRequest
        The request object, used for logging system activities.
    admin_position_pk : str, optional
        The primary key of the admin position whose permissions need to be updated.
    admin_permission_pk_list : list, optional
        A list of permission primary keys that should replace the current permissions.

    Returns:
    -------
    tuple (bool, str)
        - If the update is successful: (True, "Updated successfully")
        - If an error occurs: (False, <error_message>)

    Raises:
    ------
    Handles and logs the following exceptions:
        - DatabaseError: Raised for unexpected database errors.
        - OperationalError: Raised for unexpected server errors.
        - ProgrammingError: Raised for programming-related errors.
        - IntegrityError: Raised for database integrity constraint violations.
        - Exception: Catches any other unexpected errors.

    Process:
    -------
    1. Fetches the current admin role permissions for the given position.
    2. Retrieves the list of new permissions.
    3. Compares the existing permissions with the new ones.
    4. If there are changes:
        - Deletes the existing permissions.
        - Creates new role permissions with the updated list.
        - Logs the update process using `SystemLogs`.

    Error Handling:
    --------------
    - Logs errors in the `ErrorLogs` model with the error type and message.
    - Returns appropriate user-friendly error messages based on the exception type.

    Example Usage:
    -------------
    >>> update_admin_role_permission(request, "10", ["101", "102"])
    (True, "Updated successfully")

    >>> update_admin_role_permission(request, "10", ["101"])
    (True, "Updated successfully")

    >>> update_admin_role_permission(request, "invalid", ["101"])
    (False, "An unexpected error in Database occurred while updating admin role permission! Please try again later.")
    """

        try:
           
            admin_role_permissions,message = AdminManagement.fetch_admin_role_permission(admin_position_pk=admin_position_pk)
            existing_admin_permission_pk_list = [p.permission for p in admin_role_permissions]
            newly_added_permissions = [AdminPermissions.objects.get(pk=admin_permission_pk) for admin_permission_pk in admin_permission_pk_list]
            admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)

            if sorted(existing_admin_permission_pk_list) != sorted(newly_added_permissions):
                for p in admin_role_permissions:
                    p.delete()

                for admin_permission_pk in admin_permission_pk_list:
                    admin_permission,message = AdminManagement.fetch_admin_permissions(permission_pk=admin_permission_pk)
                    admin_role_permissions = AdminRolePermission.objects.create(role=admin_position,permission=admin_permission)
                    admin_role_permissions.save()
                    SystemLogs.updated_by(request,admin_role_permissions)
                    SystemLogs.admin_activites(request,f"Updated admin role permission {admin_role_permissions.role.name}",message="Updated")
            return True,"Updated successfully"
            
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating admin role permission! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating admin role permission! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating admin role permission! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while updating admin role permission! Please try again later.")
        
    def delete_admin_role_permission(request,admin_position_pk):

        """
    Deletes all admin role permissions associated with a given admin position.

    Parameters:
    ----------
    request : HttpRequest
        The request object, used for logging system activities.
    admin_position_pk : str
        The primary key of the admin position whose permissions need to be deleted.

    Returns:
    -------
    tuple (bool, str)
        - If the deletion is successful: (True, "Deleted successfully")
        - If an error occurs: (False, <error_message>)

    Raises:
    ------
    Handles and logs the following exceptions:
        - DatabaseError: Raised for unexpected database errors.
        - OperationalError: Raised for unexpected server errors.
        - ProgrammingError: Raised for programming-related errors.
        - IntegrityError: Raised for database integrity constraint violations.
        - Exception: Catches any other unexpected errors.

    Process:
    -------
    1. Fetches the admin position using `admin_position_pk`.
    2. Logs the deletion activity using `SystemLogs`.
    3. Deletes all `AdminRolePermission` records associated with the admin position.

    Error Handling:
    --------------
    - Logs errors in the `ErrorLogs` model with the error type and message.
    - Returns appropriate user-friendly error messages based on the exception type.

    Example Usage:
    -------------
    >>> delete_admin_role_permission(request, "10")
    (True, "Deleted successfully")

    >>> delete_admin_role_permission(request, "invalid")
    (False, "An unexpected error in Database occurred while deleting admin role permission! Please try again later.")
    """
        
        try:
            #getting the admin role permission
            admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
            SystemLogs.admin_activites(request,f"Deleted admin role permission {admin_position.name}",message="Deleted")
            AdminRolePermission.objects.filter(role=admin_position).delete()
            return True, "Deleted successfully"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting admin role permission! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting admin role permission! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting admin role permission! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while deleting admin role permission! Please try again later.")
        