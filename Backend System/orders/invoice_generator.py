from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
import os
from datetime import datetime
from decimal import Decimal
from .models import *
from django.core.files.base import ContentFile


def render_to_pdf(template_src, context_dict={}):
    """
    Render HTML template to PDF
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None
class InvoiceGenerator:
    
    @staticmethod
    def generate_invoice_number(order):
        """Generate unique invoice number based on order ID and date"""
        today = datetime.now()
        # Format: INV-{YEAR}{MONTH}{DAY}-{ORDER_ID}
        invoice_number = f"INV-{today.year}{today.month:02d}{today.day:02d}-{order.pk}"
        return invoice_number

    @staticmethod
    def get_invoice_context(order, for_email=False):
        """
        Prepare context for invoice template
        
        Args:
            order: Order model instance
            for_email: Boolean flag to indicate if this is for email (HTML) or PDF
        """
        try:
            from decimal import Decimal
            
            # Get order details
            order_details = order.items.all()
            shipping_address = order.shipping_address.first()
            payment_details = order.payment_details.first()
            
            # Calculate totals
            subtotal = sum(item.subtotal for item in order_details)
            
            # Determine if the order is paid or cancelled
            is_paid = order.order_status in ['delivered', 'shipped']
            is_cancelled = order.order_status == 'cancelled'
            
            # Format dates
            order_date = order.order_date.strftime('%b %d, %Y')
            due_date = (order.order_date.replace(day=order.order_date.day + 5)).strftime('%b %d, %Y')
            
            # Get customer info
            customer = order.customer_id
            
            # Ensure all monetary values are Decimal objects
            total_amount = Decimal(str(order.total_amount))
            paid_amount = Decimal(str(payment_details.payment_amount)) if payment_details else Decimal('0.00')
            
            context = {
                'invoice_number': InvoiceGenerator.generate_invoice_number(order),
                'order': order,
                'order_details': order_details,
                'shipping_address': shipping_address,
                'payment_details': payment_details,
                'subtotal': subtotal,
                'total': total_amount,
                'paid_amount': paid_amount,
                'balance_due': total_amount - paid_amount,
                'order_date': order_date,
                'due_date': due_date,
                'customer': customer,
                'is_paid': is_paid,
                'is_cancelled': is_cancelled,
                'for_email': for_email,
                'static_url': settings.STATIC_URL,
            }
            
            return context
        except Exception as e:
            # Log error
            from system.models import ErrorLogs
            ErrorLogs.objects.create(
                error_type="InvoiceContextError",
                error_message=f"Error preparing invoice context: {str(e)}"
            )
            raise e

    @staticmethod
    def generate_pdf_invoice(order, save_to_db=True, request=None):
        """
        Generate PDF invoice for an order
        
        Args:
            order: Order model instance
            save_to_db: Whether to save the invoice to the database
            request: The request object for logging the user who generated the invoice
            
        Returns:
            BytesIO object containing PDF data
        """
        try:
            context = InvoiceGenerator.get_invoice_context(order)
            pdf_data = render_to_pdf('invoice_template.html', context)
            
            if pdf_data and save_to_db:
                # Generate invoice number
                invoice_number = InvoiceGenerator.generate_invoice_number(order)
                
                # Check if invoice already exists
                invoice, created = Invoice.objects.get_or_create(
                    order=order,
                    invoice_number=invoice_number,
                    defaults={'is_finalized': order.order_status in ['delivered', 'shipped']}
                )
                
                # Create filename
                filename = f"Invoice_{invoice_number}.pdf"
                
                # Save PDF to FileField
                invoice.invoice_file.save(filename, ContentFile(pdf_data), save=True)
                
                # Save updated_by info if request is provided
                if request and hasattr(request, 'user') and request.user.is_authenticated:
                    updated_by = {
                        'user_id': request.user.id,
                        'username': request.user.username,
                        'email': request.user.email,
                        'timestamp': datetime.now().isoformat()
                    }
                    invoice.updated_by = updated_by
                    invoice.save()
            
            return pdf_data
        except Exception as e:
            # Log error
            from system.models import ErrorLogs
            ErrorLogs.objects.create(
                error_type="PDFGenerationError",
                error_message=f"Error generating PDF invoice: {str(e)}"
            )
            return None

    @staticmethod
    def generate_html_invoice(order):
        """
        Generate HTML invoice for email
        
        Args:
            order: Order model instance
            
        Returns:
            String containing HTML data
        """
        try:
            context = InvoiceGenerator.get_invoice_context(order, for_email=True)
            template = get_template('invoice_email_template.html')
            html = template.render(context)
            return html
        except Exception as e:
            # Log error
            from system.models import ErrorLogs
            ErrorLogs.objects.create(
                error_type="HTMLGenerationError",
                error_message=f"Error generating HTML invoice: {str(e)}"
            )
            return None
    
    @staticmethod
    def get_or_generate_invoice(order, request=None):
        """
        Get an existing invoice or generate a new one
        
        Args:
            order: Order model instance
            request: Optional request object for tracking who generated the invoice
            
        Returns:
            Invoice model instance and PDF data
        """
        try:
            # Generate invoice number
            invoice_number = InvoiceGenerator.generate_invoice_number(order)
            
            # Check if invoice already exists
            invoice = Invoice.objects.filter(order=order).order_by('-created_at').first()
            
            if invoice and invoice.invoice_file:
                # Return existing invoice if it exists and has a file
                with open(invoice.invoice_file.path, 'rb') as f:
                    pdf_data = f.read()
                return invoice, pdf_data
            else:
                # Generate new invoice
                pdf_data = InvoiceGenerator.generate_pdf_invoice(order, save_to_db=True, request=request)
                
                if not invoice:
                    # If no invoice exists yet, get the newly created one
                    invoice = Invoice.objects.filter(order=order).order_by('-created_at').first()
                    
                return invoice, pdf_data
        except Exception as e:
            # Log error
            from system.models import ErrorLogs
            ErrorLogs.objects.create(
                error_type="InvoiceRetrievalError",
                error_message=f"Error retrieving/generating invoice: {str(e)}"
            )
            return None, None