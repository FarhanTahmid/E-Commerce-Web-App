from django.urls import path
from . import views

app_name = "business_company"

urlpatterns = [
    path('company_login/',views.company_login,name="company_login"),
    path('company_register/',views.company_register,name="company_register"),
    path('company_dashboard/',views.company_dashboard,name="company_dashboard"),
]
