from django.shortcuts import render,HttpResponse,redirect
import logging
from datetime import datetime
import traceback
from django.contrib import messages
from system_administrator.system_error_handling  import ErrorHandling
from django.contrib.auth.models import User,auth
from .models import *
from .render_data import *


# Create your views here.
logger=logging.getLogger(__name__)

def company_login(request):

    try:
        company = Business_Handling.get_business_credentials()
        if request.method == "POST":

            if request.POST.get('login'):

                username = request.POST.get('username')
                password = request.POST.get('userpassword')
                #getting user credentials
                user = auth.authenticate(username=username,password=password)
                if user is not None:
                    auth.login(request,user)
                    return HttpResponse("Logged in")
                else:
                    messages.info(request,"Credentials given are wrong")
                    return redirect('business_company:company_login') 
        context = {
            'company':company
        }
        return render(request, "auth-login.html",context)
    
    except Exception as e:
        logger.error("An error occurred for user, {user} , at {datetime}".format(datetime=datetime.now()), exc_info=True)
        ErrorHandling.save_system_errors('company_login',error_name=e,error_traceback=traceback.format_exc())
        return HttpResponse("Bad Request")
    
def company_register(request):

    try:
        company = Business_Handling.get_business_credentials()

        context = {
            'company':company
        }
        return render(request,"auth-register.html",context)
    except Exception as e:
        logger.error("An error occurred for user, (during loggin in) , at {datetime}".format(datetime=datetime.now()), exc_info=True)
        ErrorHandling.save_system_errors('company_login',error_name=e,error_traceback=traceback.format_exc())
        return HttpResponse("Bad Request")