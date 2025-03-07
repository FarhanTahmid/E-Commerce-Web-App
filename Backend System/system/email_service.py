import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from django.template import Template, Context
from django.conf import settings
from .models import EmailAccounts, EmailTemplate

class EmailService:
    
    @staticmethod
    def get_email_account(purpose):
        try:
            return EmailAccounts.objects.filter(purpose=purpose, is_active=True).first()
        except EmailAccounts.DoesNotExist:
            return EmailAccounts.objects.filter(purpose='default',is_active=True).first()
    
    @staticmethod
    def get_email_template(template_name,purpose=None):
        """Get email template by name and optionally purpose"""
        query = {'name': template_name}
        if purpose:
            query['purpose'] = purpose
        
        try:
            return EmailTemplate.objects.filter(**query).first()
        except EmailTemplate.DoesNotExist:
            return None
    
    @staticmethod
    def render_template(template_content,context_data):
        template=Template(template_content)
        context=Context(context_data)
        return template.render(context)
    
    @classmethod
    def send_email(cls, to_emails, subject, text_content, html_content=None, purpose='default', 
                  template_name=None, context_data=None, from_email=None, reply_to=None, 
                  attachments=None):
        
        if isinstance(to_emails, str):
            to_emails = [to_emails]

        # Get the appropriate email account
        email_account = cls.get_email_account(purpose)
        if not email_account:
            return False
        
        # Use template if provided
        if template_name and context_data:
            template = cls.get_email_template(template_name, purpose)
            if template:
                subject = cls.render_template(template.subject, context_data)
                text_content = cls.render_template(template.body_text, context_data)
                if template.body_html:
                    html_content = cls.render_template(template.body_html, context_data)
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email or email_account.email_address
        msg['To'] = ', '.join(to_emails)
        
        if reply_to:
            msg['Reply-To'] = reply_to
        
        # Attach text and HTML parts
        msg.attach(MIMEText(text_content, 'plain'))
        if html_content:
            msg.attach(MIMEText(html_content, 'html'))
        
        # Add file attachments if provided
        if attachments:
            for attachment in attachments:
                if isinstance(attachment, dict) and 'filename' in attachment and 'content' in attachment:
                    part = MIMEApplication(attachment['content'])
                    part.add_header('Content-Disposition', 'attachment', filename=attachment['filename'])
                    msg.attach(part)
        
        # Send the email
        try:
            print(f"Email account: {email_account.email_address}")
            # Connect to SMTP server
            if email_account.use_ssl:
                server = smtplib.SMTP_SSL(email_account.smtp_server, email_account.smtp_port)
            else:
                server = smtplib.SMTP(email_account.smtp_server, email_account.smtp_port)
                
            if email_account.use_tls:
                server.starttls()
                
            # Login
            server.login(email_account.username, email_account.password)
            
            # Send the email
            server.sendmail(msg['From'], to_emails, msg.as_string())
            server.quit()

            return True
            
        except Exception as e:
            print(f"Email error: {str(e)}")
            return False
    
    @classmethod
    def send_order_confirmation_email(cls, order, invoice_pdf=None):
        """
        Send order confirmation email with invoice
        
        Args:
            order: Order model instance
            invoice_pdf: Optional PDF data to attach
        
        Returns:
            Boolean indicating success/failure
        """
        try:
            # Import here to avoid circular imports
            from orders.invoice_generator import InvoiceGenerator
            
            # Generate invoice HTML for email content
            html_content = InvoiceGenerator.generate_html_invoice(order)
            
            if not html_content:
                return False
            
            # Setup attachments
            attachments = []
            if invoice_pdf:
                attachments.append({
                    'filename': f"Invoice_{order.order_id}.pdf",
                    'content': invoice_pdf
                })
            
            # Send the email
            subject = f"Order Confirmation - {order.order_id}"
            text_content = f"Thank you for your order! Your order (ID: {order.order_id}) has been confirmed and is being processed."
            
            return cls.send_email(
                to_emails=order.customer_id.email,
                subject=subject,
                text_content=text_content,
                html_content=html_content,
                purpose='transactional',
                attachments=attachments
            )
            
        except Exception as e:
            from system.models import ErrorLogs
            ErrorLogs.objects.create(
                error_type="OrderConfirmationEmailError",
                error_message=f"Error sending order confirmation email: {str(e)}"
            )
            return False