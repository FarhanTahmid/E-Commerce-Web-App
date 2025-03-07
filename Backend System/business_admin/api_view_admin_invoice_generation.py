from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from zipfile import ZipFile
from io import BytesIO
import logging
import json
from datetime import datetime
from customer.models import Accounts
from orders.order_management import OrderManagement
from .models import Order
from orders.invoice_generator import InvoiceGenerator
from orders.models import Invoice
from system.models import ErrorLogs
from system.system_log import SystemLogs


class AdminInvoiceListView(APIView):
    """
    Admin endpoint to list and filter all invoices
    
    
    Query parameters:
    - order_id: Filter by order ID
    - customer_id: Filter by customer ID
    - customer_email: Filter by customer email
    - status: Filter by order status
    - date_from: Filter by invoice date (from)
    - date_to: Filter by invoice date (to)
    - sort_by: Sort field (created_at, order_id, customer_id, total_amount)
    - sort_order: asc or desc
    - page: Page number for pagination
    - page_size: Number of results per page
    
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
            
        try:
            # Get query parameters
            order_id = request.query_params.get('order_id')
            customer_id = request.query_params.get('customer_id')
            customer_email = request.query_params.get('customer_email')
            status = request.query_params.get('status')
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            sort_by = request.query_params.get('sort_by', 'created_at')
            sort_order = request.query_params.get('sort_order', 'desc')
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            
            # Start with all invoices
            invoices = Invoice.objects.all()
            
            # Apply filters
            if order_id:
                invoices = invoices.filter(order__order_id__icontains=order_id)
                
            if customer_id:
                invoices = invoices.filter(order__customer_id__id=customer_id)
                
            if customer_email:
                invoices = invoices.filter(order__customer_id__email__icontains=customer_email)
                
            if status:
                invoices = invoices.filter(order__order_status=status)
                
            if date_from:
                try:
                    date_from = datetime.strptime(date_from, "%Y-%m-%d")
                    invoices = invoices.filter(created_at__gte=date_from)
                except ValueError:
                    pass
                
            if date_to:
                try:
                    date_to = datetime.strptime(date_to, "%Y-%m-%d")
                    invoices = invoices.filter(created_at__lte=date_to)
                except ValueError:
                    pass
                
            # Apply sorting
            if sort_by == 'customer_id':
                sort_field = 'order__customer_id__id'
            elif sort_by == 'total_amount':
                sort_field = 'order__total_amount'
            elif sort_by == 'order_id':
                sort_field = 'order__order_id'
            else:
                sort_field = 'created_at'
                
            if sort_order.lower() == 'asc':
                invoices = invoices.order_by(sort_field)
            else:
                invoices = invoices.order_by(f'-{sort_field}')
                
            # Calculate pagination
            total_invoices = invoices.count()
            total_pages = (total_invoices + page_size - 1) // page_size
            
            # Apply pagination
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            
            invoices = invoices[start_idx:end_idx]
            
            # Prepare response data
            invoice_data = []
            for invoice in invoices:
                invoice_data.append({
                    'id': invoice.id,
                    'invoice_number': invoice.invoice_number,
                    'order_id': invoice.order.order_id,
                    'customer_id': invoice.order.customer_id.id,
                    'customer_name': f"{invoice.order.customer_id.first_name} {invoice.order.customer_id.last_name}",
                    'customer_email': invoice.order.customer_id.email,
                    'order_status': invoice.order.order_status,
                    'total_amount': float(invoice.order.total_amount),
                    'created_at': invoice.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'is_finalized': invoice.is_finalized,
                    # ###### Have to fix download URL####
                    'download_url': f'/api/admin/invoices/{invoice.id}/download/',
                })
            
            return Response({
                'invoices': invoice_data,
                'pagination': {
                    'total_items': total_invoices,
                    'total_pages': total_pages,
                    'current_page': page,
                    'page_size': page_size
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_msg = f"Error retrieving admin invoice list: {str(e)}"
            ErrorLogs.objects.create(
                error_type="AdminInvoiceListError",
                error_message=error_msg
            )
            return Response(
                {"error": "An unexpected error occurred while retrieving invoices"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AdminBulkInvoiceDownloadView(APIView):
    """
    Admin endpoint to download multiple invoices as a ZIP file
    
    POST /api/admin/invoices/bulk-download/
    
    Request body:
    {
        "invoice_ids": [1, 2, 3, ...]
    }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
            
        try:
            # Get invoice IDs from request body
            invoice_ids = request.data.get('invoice_ids', [])
            
            if not invoice_ids:
                return Response(
                    {"error": "No invoice IDs provided"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create in-memory zip file
            zip_buffer = BytesIO()
            with ZipFile(zip_buffer, 'w') as zip_file:
                # Process each invoice
                for invoice_id in invoice_ids:
                    try:
                        invoice = Invoice.objects.get(id=invoice_id)
                        
                        # If invoice has a file, add it to the ZIP
                        if invoice.invoice_file:
                            with open(invoice.invoice_file.path, 'rb') as f:
                                pdf_data = f.read()
                        else:
                            # Otherwise, generate a new PDF
                            order = invoice.order
                            pdf_data = InvoiceGenerator.generate_pdf_invoice(order, save_to_db=True, request=request)
                            
                            if not pdf_data:
                                continue
                        
                        # Add to ZIP file
                        filename = f"Invoice_{invoice.invoice_number}.pdf"
                        zip_file.writestr(filename, pdf_data)
                        
                    except Invoice.DoesNotExist:
                        continue
                    except Exception as e:
                        ErrorLogs.objects.create(
                            error_type="BulkInvoiceZipError",
                            error_message=f"Error adding invoice {invoice_id} to ZIP: {str(e)}"
                        )
                        continue
            
            # Prepare response with ZIP file
            zip_buffer.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            response = HttpResponse(zip_buffer.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="Invoices_{timestamp}.zip"'
            
            # Log the bulk download
            SystemLogs.admin_activites(request, f"Admin downloaded {len(invoice_ids)} invoices in bulk", "Downloaded")
            
            return response
            
        except Exception as e:
            error_msg = f"Error in bulk invoice download: {str(e)}"
            ErrorLogs.objects.create(
                error_type="BulkInvoiceDownloadError",
                error_message=error_msg
            )
            return Response(
                {"error": "An unexpected error occurred during bulk invoice download"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminCustomerInvoicesView(APIView):
    """
    Admin endpoint to get all invoices for a specific customer
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, customer_id):
            
        try:
            # Get the customer
            customer = get_object_or_404(Accounts, id=customer_id)
            
            # Get all invoices for this customer
            invoices = Invoice.objects.filter(order__customer_id=customer).order_by('-created_at')
            
            # Prepare response data
            invoice_data = []
            for invoice in invoices:
                invoice_data.append({
                    'id': invoice.id,
                    'invoice_number': invoice.invoice_number,
                    'order_id': invoice.order.order_id,
                    'order_status': invoice.order.order_status,
                    'total_amount': float(invoice.order.total_amount),
                    'created_at': invoice.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'is_finalized': invoice.is_finalized,
                    'download_url': f'/api/admin/invoices/{invoice.id}/download/',
                })
            
            return Response({
                'customer': {
                    'id': customer.id,
                    'name': f"{customer.first_name} {customer.last_name}",
                    'email': customer.email,
                },
                'invoices': invoice_data,
                'total_invoices': len(invoice_data)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_msg = f"Error retrieving customer invoices: {str(e)}"
            ErrorLogs.objects.create(
                error_type="AdminCustomerInvoicesError",
                error_message=error_msg
            )
            return Response(
                {"error": "An unexpected error occurred while retrieving customer invoices"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AdminGenerateInvoiceView(APIView):
    """
    Admin endpoint to generate/regenerate an invoice for an order
    
    POST /api/admin/orders/{order_id}/generate-invoice/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, order_id):
        # Check permissions
        has_permission, response = self.check_admin_permission(request)
        if not has_permission:
            return response
            
        try:
            # Get the order
            order_dict, message = OrderManagement.fetch_orders_details(order_id=order_id)
            
            if not order_dict:
                return Response({"error": message}, status=status.HTTP_404_NOT_FOUND)
            
            order = order_dict[order_id][0]
            
            # Generate the invoice with force=True to regenerate even if it exists
            pdf_data = InvoiceGenerator.generate_pdf_invoice(order, save_to_db=True, request=request)
            
            if not pdf_data:
                return Response(
                    {"error": "Failed to generate invoice PDF"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the generated invoice
            invoice = Invoice.objects.filter(order=order).order_by('-created_at').first()
            
            # Create response
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.invoice_number}.pdf"'
            
            # Log the generation
            SystemLogs.admin_activites(request, f"Admin generated invoice for order {order_id}", "Generated")
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating invoice for order {order_id}: {str(e)}"
            ErrorLogs.objects.create(
                error_type="AdminInvoiceGenerationError",
                error_message=error_msg
            )
            return Response(
                {"error": "An unexpected error occurred while generating the invoice"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )