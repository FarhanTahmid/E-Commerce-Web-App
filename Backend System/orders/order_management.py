from .models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.system_log import SystemLogs
from system.models import ErrorLogs
from products.product_management import ManageProducts
from system.manage_system import SystemManagement

class OrderManagement:

    def fetch_delivery_time(delivery_pk="",delivery_name=""):

        try:
            if delivery_pk!="":
                delivery = DeliveryTime.objects.get(pk=delivery_pk)
                return delivery, "Fetched Successfully"
            elif delivery_name!="":
                delivery = DeliveryTime.objects.filter(delivery_name=delivery_name).order_by('-pk')
                return delivery, "Fetched Successfully" if len(delivery)>0 else "No delivery time found"
            else:
                delivery = DeliveryTime.objects.all().order_by('-pk')
                return delivery, "Fetched Successfully" if len(delivery)>0 else "No delivery time found"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching delivery time! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching delivery time! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching delivery timee! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching delivery time! Please try again later.")
        
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
        
    def fetch_order_status_list():

        try:

            all_list = Order.ORDER_STATUS_CHOICES
            final_list = []
            for p in all_list:
                final_list.append(p[0][0])
            
            return final_list

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching order status list! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching order status list! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching order status list! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching order status list! Please try again later.")
        

    def fetch_orders_details(order_id="",user_name="",order_pk=""):

        try:
            dic = {}
            if order_id!="":
                order = Order.objects.get(order_id=order_id)
                order_details = OrderDetails.objects.filter(order_id = order)
                order_shipping_address = OrderShippingAddress.objects.get(order_id=order)
                order_payment = OrderPayment.objects.get(order_id=order)
                dic[order.order_id] = [order,order_details,order_shipping_address,order_payment] 
                return dic, "Order Fetched Successfully"
            elif user_name!="":
                account = Accounts.objects.get(username=user_name)
                orders = Order.objects.filter(customer_id = account).order_by('-pk')
                for o in orders:
                    order_details = OrderDetails.objects.filter(order_id = o)
                    order_shipping_address = OrderShippingAddress.objects.get(order_id=o)
                    order_payment = OrderPayment.objects.get(order_id=o)
                    dic[o.order_id] = [o, order_details,order_shipping_address,order_payment]
                return dic, "Orders Fetched Successfully" if len(orders)>0 else "No Orders found"
            elif order_pk!="":
                order = Order.objects.get(pk=order_pk)
                order_details = OrderDetails.objects.filter(order_id = order)
                order_shipping_address = OrderShippingAddress.objects.get(order_id=order)
                order_payment = OrderPayment.objects.get(order_id=order)
                dic[order.order_id] = [order,order_details,order_shipping_address,order_payment]
                return dic, "Order Fetched Successfully"
            else:
                orders = Order.objects.all().order_by('-pk')
                for o in orders:
                    order_details = OrderDetails.objects.filter(order_id = o)
                    order_shipping_address = OrderShippingAddress.objects.get(order_id=o)
                    order_payment = OrderPayment.objects.get(order_id=o)
                    dic[o.order_id] = [o, order_details,order_shipping_address,order_payment]
                return dic, "All Orders Fetched Successfully" if len(orders)>0 else "No Orders found"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching orders! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching orders! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching orders! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching orders! Please try again later.")
    
    def update_order_details(request,order_id,order_date="",delivery_time_pk="",total_amount="",order_status="",product_sku_pk="",quantity=""):

        try:
            
            #getting user order
            dictionary,message = OrderManagement.fetch_orders_details(order_id=order_id)
            order_list = dictionary[order_id]
            order = order_list[0]
            order_details = order_list[1]

            if order_date!="":
                order.order_date = order_date
            if delivery_time_pk!="":
                delivery_time,message = OrderManagement.fetch_delivery_time(delivery_pk=delivery_time_pk)
                order.delivery_time = delivery_time
            if total_amount!="":
                order.total_amount = total_amount
            if order_status!="":
                order.order_status = order_status

            if product_sku_pk!="":
                product_sku ,message = ManageProducts.fetch_product_sku(pk=product_sku_pk)

                for o in order_details:
                    if o.product_sku.pk == product_sku.pk and o.quantity != quantity:
                        price = o.product_sku.product_price
                        old_subtotal = o.subtotal
                        old_subtotal= old_subtotal - float(price * o.quantity)
                        order.total_amount = order.total_amount - float(price * o.quantity)
                        new_subtotal = old_subtotal + float(price * quantity)
                        order.total_amount = order.total_amount + float(price * quantity)

                        o.subtotal = new_subtotal
                        o.save()
                        order.save()

            SystemLogs.updated_by(request,order)
            SystemLogs.admin_activites(request,f"Order Updated, order_id - {order.order_id} ","Updated")
            
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating orders! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating orders! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating orders! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating orders! Please try again later.")
        
    def fetch_order_cancellation_requests(order_cancellation_request_pk=""):

        try:
            if order_cancellation_request_pk!="":
                cancel = CancelOrderRequest.objects.get(pk=order_cancellation_request_pk)
                return cancel,"Fetch Succesfully"
            else:
                cancel = CancelOrderRequest.objects.all().order_by('-pk')
                return cancel,"All Fetched Successfully" if len(cancel)>0 else "No Request Made Yet"
            
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching cancellation order! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching cancellation order! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching cancellation order! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while cancelling order! Please try again later.")
        
    def order_cancellation_request(request,order_cancellation_pk,status=False):

        try:
            order_cancel,message = OrderManagement.fetch_order_cancellation_requests(order_cancellation_request_pk=order_cancellation_pk)
            if status:
                order_details = OrderDetails.objects.filter(order_id=order_cancel.order_id)
                for detail in order_details:
                    detail.product_sku.product_stock += detail.quantity
                    detail.product_sku.save()

                payment = OrderPayment.objects.get(order_id=order_cancel.order_id)
                if payment.payment_status == 'success':
                    payment.payment_status = 'refunded'
                    payment.save()

                #restore coupon if used
                if payment.coupon_applied:
                    payment.coupon_applied.usage_limit+=1
                    payment.coupon_applied.save()
                    payment.save()

            SystemLogs.updated_by(request,order_cancel.order_id)
            SystemLogs.admin_activites(request,f"Order Cancelled, order_id - {(order_cancel.order_id)} ","Cancelled")
            SystemManagement.send_email("Order Cancelled","Your Order has been cancelled",[order_cancel.order_id.customer_id.email],[],"","",request)
            SystemManagement.create_notification(title="Order Cancelled",user_names=[order_cancel.order_id.customer_id.username],description="Your Order has been cancelled",request=request)
            order_cancel.order_id.delete()
            
            return True, "Order Cancelled Succesfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while cancelling order! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while cancelling order! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while cancelling order! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while cancelling order! Please try again later.")