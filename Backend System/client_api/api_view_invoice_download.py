from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from orders.models import Invoice
from system.system_log import SystemLogs
from orders.order_management import OrderManagement
from system.models import ErrorLogs
from orders.invoice_generator import InvoiceGenerator

class UserInvoiceDownloadView(APIView):
    """
    Customer endpoint to download their invoice
    
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_id):
        try:
            # Get the order
            order_dict, message = OrderManagement.fetch_orders_details(order_id=order_id)
            
            if not order_dict:
                return Response({"error": message}, status=status.HTTP_404_NOT_FOUND)
            
            order = order_dict[order_id][0]
            
            # Check if this user owns the order
            if request.user.pk != order.customer_id.pk:
                return Response(
                    {"error": "You don't have permission to access this invoice"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get or generate the invoice
            invoice, pdf_data = InvoiceGenerator.get_or_generate_invoice(order, request)
            
            if not pdf_data:
                return Response(
                    {"error": "Failed to generate invoice PDF"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create HTTP response with PDF content
            invoice_filename = f"Invoice_{invoice.invoice_number}.pdf"
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{invoice_filename}"'
            
            # Log the download
            SystemLogs.admin_activites(None, f"Customer downloaded invoice for order {order_id}", "Downloaded")
            
            return response
            
        except Exception as e:
            error_msg = f"Error downloading invoice for order {order_id}: {str(e)}"
            ErrorLogs.objects.create(
                error_type="UserInvoiceDownloadError",
                error_message=error_msg
            )
            return Response(
                {"error": "An unexpected error occurred while downloading the invoice"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserInvoicePreviewView(APIView):
    """
    Customer endpoint to preview their invoice in HTML format
    
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_id):
        try:
            # Get the order
            order_dict, message = OrderManagement.fetch_orders_details(order_id=order_id)
            
            if not order_dict:
                return Response({"error": message}, status=status.HTTP_404_NOT_FOUND)
            
            order = order_dict[order_id][0]
            
            # Check if this user owns the order
            if request.user.pk != order.customer_id.pk:
                return Response(
                    {"error": "You don't have permission to access this invoice"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Generate HTML preview
            html_content = InvoiceGenerator.generate_html_invoice(order)
            
            if not html_content:
                return Response(
                    {"error": "Failed to generate invoice preview"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Return HTML response
            return HttpResponse(html_content, content_type='text/html')
            
        except Exception as e:
            error_msg = f"Error generating invoice preview for order {order_id}: {str(e)}"
            ErrorLogs.objects.create(
                error_type="InvoicePreviewError",
                error_message=error_msg
            )
            return Response(
                {"error": "An unexpected error occurred while generating the invoice preview"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserInvoiceListView(APIView):
    """
    Customer endpoint to list all their invoices
    
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Get all invoices for the current user
            invoices = Invoice.objects.filter(order__customer_id=request.user).order_by('-created_at')
            
            # Prepare response data
            invoice_data = []
            for invoice in invoices:
                invoice_data.append({
                    'id': invoice.id,
                    'invoice_number': invoice.invoice_number,
                    'order_id': invoice.order.order_id,
                    'order_date': invoice.order.order_date.strftime("%Y-%m-%d"),
                    'order_status': invoice.order.order_status,
                    'total_amount': float(invoice.order.total_amount),
                    'created_at': invoice.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'download_url': f'/api/orders/{invoice.order.order_id}/invoice/',
                    'preview_url': f'/api/orders/{invoice.order.order_id}/invoice/preview/',
                })
            
            return Response({
                'invoices': invoice_data,
                'total_invoices': len(invoice_data)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_msg = f"Error retrieving user invoice list: {str(e)}"
            ErrorLogs.objects.create(
                error_type="UserInvoiceListError",
                error_message=error_msg
            )
            return Response(
                {"error": "An unexpected error occurred while retrieving your invoices"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )