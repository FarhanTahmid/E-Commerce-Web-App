from django.shortcuts import render,HttpResponse,redirect
import logging
from datetime import datetime
import traceback
from django.contrib import messages
from system_administrator.system_error_handling  import ErrorHandling
from django.contrib.auth.models import User,auth
from .models import *
from .render_data import *
from django.contrib.auth.decorators import login_required


# Create your views here.
logger=logging.getLogger(__name__)

def company_login(request):

    try:
        company = Business_Handling.get_business_credentials()
        if request.method == "POST":

            if request.POST.get('login'):

                user_id = request.POST.get('username')
                password = request.POST.get('userpassword')
                #getting user credentials
                user = auth.authenticate(username=user_id,password=password)
                if user is not None:
                    auth.login(request,user)
                    return redirect('business_company:company_dashboard')
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

        if request.method == "POST":

            if request.POST.get('register_user'):

                employee_user_id = request.POST.get('username')
                password = request.POST.get('user_password')
                confirm_password = request.POST.get('user_confirm_password')

                #sending the data to validate user and returning a tuple where first index is always
                #True or False and second index could be message or object
                result = Login.register_user(employee_user_id,password,confirm_password)

                if result[0]:
                    auth.login(request,result[1])
                    return redirect('business_company:company_dashboard')
                else:
                    messages.info(request,result[1])
                    return redirect('business_company:company_register')                

        context = {
            'company':company
        }
        return render(request,"auth-register.html",context)
    except Exception as e:
        logger.error("An error occurred for user, (during loggin in) , at {datetime}".format(datetime=datetime.now()), exc_info=True)
        ErrorHandling.save_system_errors('company_login',error_name=e,error_traceback=traceback.format_exc())
        return HttpResponse("Bad Request")
    
@login_required
def company_dashboard(request):

    try:
        #getting current logged in user
        user = request.user.username
        company = Business_Handling.get_business_credentials()

        context = {
            'company':company
        }
        return render(request,'apps-kanban-board.html',context)
    except Exception as e:
        logger.error("An error occurred for user, (during loggin in) , at {datetime}".format(datetime=datetime.now()), exc_info=True)
        ErrorHandling.save_system_errors(user,error_name=e,error_traceback=traceback.format_exc())
        return HttpResponse("Bad Request")