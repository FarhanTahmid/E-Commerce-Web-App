from business_company.models import *
import logging
from django.contrib.auth .models import User
from datetime import datetime
import traceback
from system_administrator.system_error_handling  import ErrorHandling

logger=logging.getLogger(__name__)

class Business_Handling:
    
    def create_business(**kwargs):
        """Creates a new business."""
        # function returns messages and the function status.
        
        if(Business_Identity.objects.exists()):
            message="A business already exists!"
            func_status=False
            return message,func_status
        else: 
            new_business=Business_Identity.objects.create(
                platform_product_key=kwargs['product_key'],
                business_name=kwargs['business_name'],
                business_logo=kwargs['business_logo'],
                business_description=kwargs['business_description']
            )
            new_business.save()
            message="New business created!"
            func_status=True
            return message,func_status
        
    def get_business_credentials():

        return Business_Identity.objects.first()

class Login:

    def register_user(user_name,password,confirm_password):
        '''Registers a user to the database if he is not registered yet'''
        
        #declaring a message variable to return different message according to condition
        message = ""

        if password == confirm_password:

            if len(password)>6:

                try:

                    get_employee = Comapany_Users.objects.get(employee_id = user_name)

                    #checking if user is already signed up
                    if User.objects.filter(username = user_name).exists():
                        message = "You are already signed up! Try Logging in instead."
                        return (False,message)
                    else:
                        #user not signed up so creating new User

                        try:
                            user = User.objects.create_user(username=user_name,email = get_employee.email,password = password)
                            user.save()
                            return (True,user)
                        except:
                            message = "Something went wrong! Try again"
                            return (False,message) 
                        
                except Comapany_Users.DoesNotExist:
                    message = "Looks like you are not a registered Employee.\n"+ \
                               "Contact your company's IT department for assistance."
                    return  (False,message)  
            else:
                message = "Password must be greater than 6 characters"
                return  (False,message)
        else:
            message = "Passwords did not match. Try again"
            return (False,message)


        


            