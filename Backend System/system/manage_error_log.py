from datetime import datetime
from .models import *
class ManageErrorLog:
    def create_error_log(error_type,error_message):
        '''This function creates an error log in the database'''
        try:
            # Create error log
            timestamp = datetime.now()
            new_error_log = ErrorLogs(timestamp=timestamp, error_type=error_type, error_message=error_message)
            new_error_log.save()
            return True
        except ValueError:
            return None
        except Exception as e:
            print(e)
        