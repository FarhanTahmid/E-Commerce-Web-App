from .models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.models import *
from system.system_log import SystemLogs
from e_commerce_app import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import os

class AdminManagement:

    #admin position
    def fetch_admin_position(pk="",name=""):

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
        
    #admin permissions
    def fetch_admin_permissions(permission_name=""):
        try:
            if permission_name!="":
                permission_name = permission_name.lower()
                permission =  AdminPermissions.objects.get(permission_name = permission_name)
                return permission, "Permission fetched successfully"
            else:
                permission = AdminPermissions.objects.all()
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

        try:
            #exisitng permissions
            permission_name = permission_name.lower()
            permission,message = AdminManagement.fetch_admin_permissions(permission_name=permission_name)
            if not permission:
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
                return True, "Admin permission created successfully"
            else:
                return False,"Admin permission with this name already exists"


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
    
    def create_business_admin_user(admin_full_name,password,admin_position_pk,
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
            admin_position_pk (int): The primary key (ID) of the admin position to be associated with the admin user.
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
                admin_position_pk=1,
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
        try:
            #fetching all to check if this user
            all_admins,message = AdminManagement.fetch_business_admin_user()
            if any(p.admin_email == admin_email for p in all_admins):
                return False, "Admin with this email already exists"
            admin_user_name = admin_email.split('@')[0]
            admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
            business_admin = BusinessAdminUser.objects.create(admin_full_name=admin_full_name,admin_user_name=admin_user_name,
                                                              admin_position = admin_position)
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

    def update_business_admin_user(request,admin_unique_id,admin_full_name,admin_position_pk,admin_email,
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
            admin_position_pk (int): The primary key (ID) of the new admin position to be associated with the admin user.
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
                admin_position_pk=1,
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
            business_admin_user,message = AdminManagement.fetch_business_admin_user(admin_unique_id=admin_unique_id)
            all_business_admin_user,message = AdminManagement.fetch_business_admin_user()
            admin_position,message = AdminManagement.fetch_admin_position(pk=admin_position_pk)
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
            if business_admin_user.admin_full_name.lower() != admin_full_name.lower():
                business_admin_user.admin_full_name = admin_full_name
            if business_admin_user.admin_position != admin_position:
                business_admin_user.admin_position = admin_position
            if admin_contact_no:
                if not business_admin_user.admin_contact_no or business_admin_user.admin_contact_no != admin_contact_no:
                    business_admin_user.admin_contact_no = admin_contact_no
            if admin_email and business_admin_user.admin_email != admin_email:
                for p in all_business_admin_user:
                    if p != business_admin_user and p.admin_email == admin_email:
                        return False, "This email is already taken"
                business_admin_user.admin_user_name = admin_email.split('@')[0]
                business_admin_user.admin_email = admin_email
                user.email = admin_email
                user.username = admin_email.split('@')[0]
            if admin_avatar != "":
                if not business_admin_user.admin_avatar or business_admin_user.admin_avatar != admin_avatar:
                    if business_admin_user.admin_avatar:
                        path = settings.MEDIA_ROOT+str(business_admin_user.admin_avatar)
                        if os.path.exists(path):
                            os.remove(path)
                        business_admin_user.admin_avatar.delete()
                business_admin_user.admin_avatar = admin_avatar
            business_admin_user.save()
            user.save()
            updated,message = SystemLogs.updated_by(request,business_admin_user)
            activity_updated, message = SystemLogs.admin_activites(request,f"Updated admin {business_admin_user.admin_user_name}",message="Updated")
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
        
    def update_business_admin_user_password(request,admin_unique_id,old_password,new_password):

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
            business_admin_user,message = AdminManagement.fetch_business_admin_user(admin_unique_id=admin_unique_id)
            user = Accounts.objects.get(username = business_admin_user.admin_user_name)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
            else:
                return False, "Old password is incorrect"
            updated,message = SystemLogs.updated_by(request,business_admin_user)
            activity_updated, message = SystemLogs.admin_activites(request,f"Updated admin password {business_admin_user.admin_user_name}",message="Updated password")
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
            updated,message = SystemLogs.updated_by(request,business_admin_user)
            activity_updated, message = SystemLogs.admin_activites(request,f"Reset admin password {business_admin_user.admin_user_name}",message="Reset password")
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
            activity_updated, message = SystemLogs.admin_activites(request,f"Deleted admin {business_admin_user.admin_user_name}",message="Deleted")
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