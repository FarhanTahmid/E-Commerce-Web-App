import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    
