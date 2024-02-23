from django.contrib.auth .models import User
import logging
from django.conf import settings
from datetime import datetime
from .models import SystemErrors
from e_commerce_app.settings import DEBUG

class ErrorHandling:
    
    logger=logging.getLogger(__name__)
    
    def save_system_errors(user,error_name,error_traceback):
        try:
            new_error=SystemErrors.objects.create(
                date_time=datetime.now(),
                error_name=error_name,
                error_traceback=error_traceback,
                error_occured_for = user
            )
            new_error.save()
            if(DEBUG):
                pass
            else:
                #send email to devlopers
                pass
        except:
            ErrorHandling.logger.error("An error occurred for user, {user} , at {datetime}".format(datetime=datetime.now()), exc_info=True)
    