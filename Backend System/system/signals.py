from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from business_admin.models import *
from .models import *

@receiver(user_logged_in)
def update_last_login_at(sender, request, user, **kwargs):
    try:
        if isinstance(user,Accounts):
            user = Accounts.objects.get(pk=user.pk)
            user.last_login = now()
            user.save()
    except Accounts.DoesNotExist:
        # Handle the case where no BusinessAdminUser is associated with the logged-in user
        pass