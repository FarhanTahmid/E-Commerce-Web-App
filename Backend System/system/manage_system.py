from .models import *
from django.utils import timezone
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from .system_log import SystemLogs

class SystemManagement:
    
    def fetch_notifications(read,user_name="",title=""):

        try:
            if user_name!="":
                user = Accounts.objects.prefetch_related('notifications').get(username=user_name)
                notifications = user.notifications.all().order_by('-pk')
                return notifications, "Fetched successfully" if len(notifications)>0 else "No notifications Found"
            elif title!="":
                notifications = Notification.objects.filter(title=title).order_by('-pk')
                return notifications, "Fetched successfully" if len(notifications)>0 else "No notifications Found"
            elif not read:
                notifications = Notification.objects.filter(read=False).order_by('-pk')
                return notifications, "Fetched successfully" if len(notifications)>0 else "No notifications Found"
            elif read:
                notifications = Notification.objects.filter(read=True).order_by('-pk')
                return notifications, "Fetched successfully" if len(notifications)>0 else "No notifications Found"
            else:
                notifications = Notification.objects.all().order_by('-pk')
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
        
    def create_notification(request,title,user_names=[],description="",link=""):

        try:
            if len(user_names) == 0:
                return False, "No users to send notification to"
            #appending all users
            users_list = []
            for user in user_names:
                user_ = Accounts.objects.get(username=user)
                users_list.append(user_)
            
            notification = Notification.objects.create(title=title)
            notification.save()

            notification.to.add(*users_list)
            if description!="":
                notification.description = description
            if link!="":
                notification.link = link
            
            notification.save()
            SystemLogs.updated_by(request,notification)
            SystemLogs.admin_activites(request,"Notification created","Created")
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