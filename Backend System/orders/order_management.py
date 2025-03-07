from .models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.system_log import SystemLogs
from system.models import ErrorLogs
from products.product_management import ManageProducts
from system.manage_system import SystemManagement
from system.email_service import EmailService
from .invoice_generator import InvoiceGenerator
from django.http import HttpResponse
from django.template.loader import render_to_string

class OrderManagement:

    def fetch_delivery_partner(delivery_partner_pk="",delivery_partner_name=""):

        try:
            if delivery_partner_pk!="":
                delivery = DeliveryPartner.objects.get(pk=delivery_partner_pk)
                return delivery, "Fetched Successfully"
            elif delivery_partner_name!="":
                delivery = DeliveryPartner.objects.filter(delivery_partner_name=delivery_partner_name).order_by('-pk')
                return delivery, "Fetched Successfully" if len(delivery)>0 else "No delivery partner found"
            else:
                delivery = DeliveryPartner.objects.all().order_by('-pk')
                return delivery, "Fetched Successfully" if len(delivery)>0 else "No delivery partner found"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching delivery partner! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching delivery partner! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching delivery partner! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching delivery partner! Please try again later.")
        
    def create_delivery_partner(request,delivery_partner_name):

        try:
            all_delivery_partners ,message = OrderManagement.fetch_delivery_partner()
            if any((p.delivery_partner_name.lower() == delivery_partner_name.lower()) for p in all_delivery_partners):
                return False, "Delivery Partner with this name already exists"
            delivery_parnter = DeliveryPartner.objects.create(
                delivery_partner_name = delivery_partner_name
            )
            delivery_parnter.save()
            SystemLogs.updated_by(request,delivery_parnter)
            SystemLogs.admin_activites(request,f"Delivery Partner Created, title - {delivery_parnter} ","Created")
            return True, "Created Successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating delivery partner! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating delivery partner! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating delivery partner! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while creating delivery partner! Please try again later.")
        
    def update_delivery_partner(request,delivery_partner_pk,delivery_partner_name=""):

        try:
            #getting delivery partner
            delivery_partner,message = OrderManagement.fetch_delivery_partner(delivery_partner_pk=delivery_partner_pk)
            all_delivery_partners,message = OrderManagement.fetch_delivery_partner()

            if delivery_partner_name!="":
                if any(p!=delivery_partner and p.delivery_partner_name.lower() == delivery_partner_name.lower() for p in all_delivery_partners):
                    return False, "Delivery Partner with this name already exists"
                delivery_partner.delivery_partner_name = delivery_partner_name
                delivery_partner.save()

            SystemLogs.updated_by(request,delivery_partner)
            SystemLogs.admin_activites(request,f"Delivery Partner Updated, title - {delivery_partner.delivery_partner_name} ","Updated")

            return True, "Updated Successfully"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating delivery partner! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating delivery partner! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating delivery partner! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating delivery partner! Please try again later.")
        
    def delete_delivery_partner(request,delivery_partner_pk):

        try:
            
            delivery_partner,message = OrderManagement.fetch_delivery_partner(delivery_partner_pk=delivery_partner_pk)
            delivery_partner.delete()
            return True, "Deleted Successfully"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating delivery partner! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating delivery partner! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating delivery partner! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating delivery partner! Please try again later.")

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
                "ProgrammingError": "An unexpected error in server occurred while fetching delivery time! Please try again later.",
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
        

    def fetch_orders_details(order_id="",user_name="",order_pk="",order_status=""):

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
            elif order_status!="":
                order = Order.objects.filter(order_status=order_status)
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
    
    @staticmethod
    def update_order_details(request, order_id, order_date="", delivery_time_pk="", delivery_partner_pk="", total_amount="", order_status="", product_sku_pk="", quantity=""):
        try:
            # getting user order
            dictionary, message = OrderManagement.fetch_orders_details(order_id=order_id)
            order_list = dictionary[order_id]
            order = order_list[0]
            order_details = order_list[1]

            # if order status changed to confirmed must choose delivery partner
            if order_status != "":
                previous_status = order.order_status
                order.order_status = order_status

                if order_status == 'confirmed':
                    if delivery_partner_pk == "":
                        return False, "No delivery Partner Selected"
                    
                    # Get or create delivery partner
                    delivery_partner, message = OrderManagement.fetch_delivery_partner(delivery_partner_pk=delivery_partner_pk)
                    order.delivery_partner = delivery_partner
                    
                    # Generate invoice HTML for email
                    try:
                        invoice_html = InvoiceGenerator.generate_html_invoice(order)
                        
                        # Send confirmation email with invoice
                        is_email_sent = EmailService.send_email(
                            to_emails=[order.customer_id.email], 
                            subject=f"Your Order {order.order_id} has been confirmed",
                            text_content="Your order has been confirmed. Please see the attached invoice for details.",
                            html_content=invoice_html
                        )
                        
                        # Create notification for the customer
                        notification_to_client = SystemManagement.create_notification(
                            title=f"Your Order {order.order_id} has been confirmed", 
                            user_names=[order.customer_id.username],
                            description="Your order has been confirmed and is being processed.",
                            request=request
                        )
                        
                        if not is_email_sent:
                            # Log email failure but continue
                            ErrorLogs.objects.create(
                                error_type="EmailSendError",
                                error_message=f"Failed to send order confirmation email for order {order.order_id}"
                            )
                    except Exception as e:
                        # Log error but continue with order processing
                        ErrorLogs.objects.create(
                            error_type="InvoiceGenerationError",
                            error_message=f"Error generating invoice for order {order.order_id}: {str(e)}"
                        )

                elif order_status == 'cancelled':
                    # Restore product stock quantities
                    for detail in order_details:
                        if detail.product_sku:
                            detail.product_sku.product_stock += detail.quantity
                            detail.product_sku.save()
                    
                    # Update payment status if needed
                    try:
                        payment = order.payment_details.first()
                        if payment and payment.payment_status == 'success':
                            payment.payment_status = 'refunded'
                            payment.save()
                        
                        # Restore coupon if used
                        if payment and payment.coupon_applied:
                            payment.coupon_applied.usage_limit += 1
                            payment.coupon_applied.save()
                    except Exception as e:
                        ErrorLogs.objects.create(
                            error_type="PaymentUpdateError",
                            error_message=f"Error updating payment status for cancelled order {order.order_id}: {str(e)}"
                        )
                    
                    # Send cancellation email
                    is_email_sent = EmailService.send_email(
                        to_emails=[order.customer_id.email],
                        subject=f"Your Order {order.order_id} has been cancelled",
                        text_content="Your order has been cancelled. Please contact customer support for further details."
                    )
                    
                    # Create notification
                    notification_to_client = SystemManagement.create_notification(
                        title=f"Your Order {order.order_id} has been cancelled",
                        user_names=[order.customer_id.username],
                        description="Your order has been cancelled. Please contact customer support for further details.",
                        request=request
                    )
                
                # Log the status change
                SystemLogs.admin_activites(
                    request,
                    f"Order status changed from {previous_status} to {order_status}, order_id - {order.order_id}",
                    "Updated"
                )
                
                order.save()

            # Other update operations
            if order_date != "":
                order.order_date = order_date
                
            if delivery_time_pk != "":
                delivery_time, message = OrderManagement.fetch_delivery_time(delivery_pk=delivery_time_pk)
                order.delivery_time = delivery_time
                
            if total_amount != "":
                order.total_amount = total_amount

            if product_sku_pk != "" and quantity != "":
                product_sku, message = ManageProducts.fetch_product_sku(pk=product_sku_pk)

                for o in order_details:
                    if o.product_sku and o.product_sku.pk == product_sku.pk and o.quantity != quantity:
                        price = o.product_sku.product_price
                        old_subtotal = o.subtotal
                        old_subtotal = old_subtotal - float(price * o.quantity)
                        order.total_amount = order.total_amount - float(price * o.quantity)
                        new_subtotal = old_subtotal + float(price * quantity)
                        order.total_amount = order.total_amount + float(price * quantity)

                        o.subtotal = new_subtotal
                        o.quantity = quantity
                        o.save()
                        order.save()

            SystemLogs.updated_by(request, order)
            SystemLogs.admin_activites(request, f"Order Updated, order_id - {order.order_id}", "Updated")
            return True, "Updated Successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__
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
    @staticmethod
    def generate_invoice_pdf(order_id):
        """
        Generate a PDF invoice for an order
        
        Args:
            order_id: Order ID string
            
        Returns:
            HttpResponse with PDF attachment or error message
        """
        try:
            # Get order details
            dictionary, message = OrderManagement.fetch_orders_details(order_id=order_id)
            
            if not dictionary:
                return False, "Order not found"
                
            order_list = dictionary[order_id]
            order = order_list[0]
            
            # Generate PDF
            pdf = InvoiceGenerator.generate_pdf_invoice(order)
            
            if not pdf:
                return False, "Failed to generate invoice PDF"
            
            # Create HTTP response with PDF content
            invoice_filename = f"Invoice_{order_id}.pdf"
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{invoice_filename}"'
            
            # Log the invoice download
            SystemLogs.admin_activites(None, f"Invoice downloaded for order {order_id}", "Downloaded")
            
            return response
            
        except Exception as error:
            # Log the error
            error_type = type(error).__name__
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")
            
            return False, f"An unexpected error occurred while generating invoice: {error_message}"

    @staticmethod
    def get_invoice_html(order_id):
        """
        Get HTML invoice for preview
        
        Args:
            order_id: Order ID string
            
        Returns:
            HTTP response with HTML content or error message
        """
        try:
            # Get order details
            dictionary, message = OrderManagement.fetch_orders_details(order_id=order_id)
            
            if not dictionary:
                return False, "Order not found"
                
            order_list = dictionary[order_id]
            order = order_list[0]
            
            # Generate invoice context
            context = InvoiceGenerator.get_invoice_context(order, for_email=True)
            
            # Render template
            html_content = render_to_string('orders/invoice_template.html', context)
            
            # Create HTTP response
            response = HttpResponse(html_content, content_type='text/html')
            
            return response
            
        except Exception as error:
            # Log the error
            error_type = type(error).__name__
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")
            
            return False, f"An unexpected error occurred while generating invoice HTML: {error_message}"
        
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
        
    def update_order_cancellation_request(request,order_cancellation_pk,status=False):

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
                print("cancelled")
            SystemLogs.updated_by(request,order_cancel.order_id)
            SystemLogs.admin_activites(request,f"Order Cancelled, order_id - {(order_cancel.order_id)} ","Cancelled")
            is_email_sent=EmailService.send_email(
                to_emails=[order_cancel.order_id.customer_id.email],subject="Order Cancelled",text_content="Your Order has been cancelled"
            )
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