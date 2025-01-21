from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from business_admin.models import *

@receiver(user_logged_in)
def update_last_login_at(sender, request, user, **kwargs):
    try:
        # Get the BusinessAdminUser associated with the logged-in user
        business_admin_user = BusinessAdminUser.objects.get(user=user)
        # Update the last_login_at field
        business_admin_user.last_login_at = now()
        business_admin_user.save()
    except BusinessAdminUser.DoesNotExist:
        # Handle the case where no BusinessAdminUser is associated with the logged-in user
        pass