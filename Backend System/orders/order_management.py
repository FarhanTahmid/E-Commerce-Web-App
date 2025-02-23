from .models import DeliveryTime
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.system_log import SystemLogs
from system.models import ErrorLogs

class OrderManagement:

    def fetch_delivery_time(delivery_pk="",delivery_name=""):

        # try:
            if delivery_pk!="":
                delivery = DeliveryTime.objects.get(pk=delivery_pk)
                return delivery, "Fetched Successfully"
            elif delivery_name!="":
                delivery = DeliveryTime.objects.filter(delivery_name=delivery_name).order_by('-pk')
                return delivery, "Fetched Successfully" if len(delivery)>0 else "No delivery time found"
            else:
                delivery = DeliveryTime.objects.all().order_by('-pk')
                return delivery, "Fetched Successfully" if len(delivery)>0 else "No delivery time found"

        # except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
        #     # Log the error
        #     error_type = type(error).__name__  # Get the name of the error as a string
        #     error_message = str(error)
        #     ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
        #     print(f"{error_type} occurred: {error_message}")

        #     # Return appropriate messages based on the error type
        #     error_messages = {
        #         "DatabaseError": "An unexpected error in Database occurred while fetching delivery time! Please try again later.",
        #         "OperationalError": "An unexpected error in server occurred while fetching delivery time! Please try again later.",
        #         "ProgrammingError": "An unexpected error in server occurred while fetching delivery timee! Please try again later.",
        #         "IntegrityError": "Same type exists in Database!",
        #     }
        #     return False, error_messages.get(error_type, "An unexpected error occurred while fetching delivery time! Please try again later.")
        
    def create_delivery_time(request,delivery_name,estimated_time):

        try:
            all_delivery_times ,message = OrderManagement.fetch_delivery_time()
            if any((p.delivery_name.lower() == delivery_name.lower()) for p in all_delivery_times):
                return False, "Delivery Time with this name already exists"
            delivery_time = DeliveryTime.objects.create(
                delivery_name = delivery_name,
                estimated_delivery_time = estimated_time
            )
            delivery_time.save()
            SystemLogs.updated_by(request,delivery_time)
            SystemLogs.admin_activites(request,f"Delivery Time Created, title - {delivery_name} ","Created")
            return True, "Created Successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating delivery time! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating delivery time! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating delivery time! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while creating delivery time! Please try again later.")
    
    def update_delivery_time(request,delivery_time_pk,delivery_name="",estimated_time=""):

        try:
            #getting delivery time
            delivery_time,message = OrderManagement.fetch_delivery_time(delivery_pk=delivery_time_pk)
            all_delivery_times,message = OrderManagement.fetch_delivery_time()

            if delivery_name!="":
                if any(p!=delivery_time and p.delivery_name.lower()==delivery_name.lower() for p in all_delivery_times):
                    return False, "Delivery Time with this name already exists"
                delivery_time.delivery_name = delivery_name

            if estimated_time!="":
                delivery_time.estimated_delivery_time = estimated_time
            delivery_time.save()
            SystemLogs.updated_by(request,delivery_time)
            SystemLogs.admin_activites(request,f"Delivery Time Updated, title - {delivery_time.delivery_name} ","Updated")

            return True, "Updated Successfully"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating delivery time! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating delivery time! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating delivery time! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating delivery time! Please try again later.")
        
    def delete_delivery_time(request,delivery_pk):
        try:
            
            delivery_time,message = OrderManagement.fetch_delivery_time(delivery_pk=delivery_pk)
            delivery_time.delete()
            return True, "Deleted Successfully"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting delivery time! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting delivery time! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting delivery time! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while deleting delivery time! Please try again later.")