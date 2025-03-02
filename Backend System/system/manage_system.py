from .models import *
from django.utils import timezone
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from .system_log import SystemLogs
from django.core.mail import EmailMultiAlternatives
from e_commerce_app import settings
from business_admin.models import AdminPermissions,AdminUserRole

class SystemManagement:
    
    def fetch_notifications_of_user(read="",user_name="",notification_pk=""):

        try:
            if user_name!="" and read == "f":
                user = Accounts.objects.get(username = user_name)
                notifications = NotificationTo.objects.filter(to=user,read=False).order_by('-pk')
                return notifications, "Fetched successfully" if len(notifications)>0 else "No notifications Found"
            elif user_name!="" and read == "t":
                user = Accounts.objects.get(username = user_name)
                notifications = NotificationTo.objects.filter(to=user,read=True).order_by('-pk')
                return notifications, "Fetched successfully" if len(notifications)>0 else "No notifications Found"
            elif user_name!="":
                user = Accounts.objects.get(username = user_name)
                notifications = NotificationTo.objects.filter(to=user).order_by('-pk')
                return notifications, "Fetched successfully" if len(notifications)>0 else "No notifications Found"
            elif notification_pk!="":
                notification = SystemManagement.fetch_notifications(notification_pk=notification_pk)
                notifications_to = NotificationTo.objects.filter(notification=notification)
                return notifications_to, "Fetched successfully" if len(notifications_to)>0 else "No notifications Found"
            else:
                notifications = NotificationTo.objects.all().order_by('-pk')
                return notifications, "All Notifications Fetched successfully" if len(notifications)>0 else "No notifications Found"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching notifications! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching notifications! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching notifications! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching notifications! Please try again later.")
        
    def fetch_notifications(title="",notification_pk=""):

        try:
            if title!="" :
                notifications = Notification.objects.filter(title=title).order_by('-pk')
                return notifications, "Fetched successfully" if len(notifications)>0 else "No notifications Found"
            elif notification_pk!="":
                notifications = Notification.objects.get(pk=notification_pk)
                return notifications, "Fetched successfully"
            
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching notifications! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching notifications! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching notifications! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching notifications! Please try again later.")


    def create_notification(title,user_names=[],description="",link="",request=None,role=""):

        try:
            if len(user_names) == 0 and role=="":
                return False, "No users to send notification to"

            notification = Notification.objects.create(title=title)
            if description!="":
                    notification.description = description
            if link!="":
                notification.link = link
            notification.save()
            SystemLogs.updated_by(request,notification)
            SystemLogs.admin_activites(request,f"Notification created, title- {title}","Created")

            if role == "":
                for user in user_names:
                    user_ = Accounts.objects.get(username=user)
                    notification_to = NotificationTo.objects.create(to=user_,notification=notification)
                    notification_to.save()
                    
                    if request:
                        SystemLogs.updated_by(request,notification_to)
                        SystemLogs.admin_activites(request,f"Notification created for user {user_.username}, title- {title}","Created")
            else:
                role = AdminUserRole.objects.filter(role__name = role)
                for r in role:
                    user_ = r.user
                    notification_to = NotificationTo.objects.create(to=user_,notification=notification)
                    notification_to.save()
                    if request:
                        SystemLogs.updated_by(request,notification_to)
                        SystemLogs.admin_activites(request,f"Notification created for user {user_.username}, title- {title}","Created")

            
            return True, "Nofication created successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating notifications! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating notifications! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating notifications! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while creating notifications! Please try again later.")
        
    def register_all_page_permissions(request,permission_page_name_list = []):

        try:
            for p in permission_page_name_list:
                AdminPermissions.objects.get_or_create(permission_name=p.lower())

            #this permissions are for the Admin Roles - Manager, Owner... Default permissions to role
            AdminPermissions.objects.get_or_create(permission_name='view')
            AdminPermissions.objects.get_or_create(permission_name='change')

            return True, "Created Successfully"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while register permission pages! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while register permission pages! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while register permission pages! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while register permission pages! Please try again later.")