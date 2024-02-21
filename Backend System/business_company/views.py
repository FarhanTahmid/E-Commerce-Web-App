from django.shortcuts import render

# Create your views here.
def company_login(request):
    return render(request, "auth-login.html")