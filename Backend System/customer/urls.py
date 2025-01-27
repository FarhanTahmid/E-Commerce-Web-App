from django.urls import path
from .views import *

app_name = 'customer'

urlpatterns = [
    path('signup/', CustomerSignupView.as_view(), name='signup'),
    path('login/',CustomerLoginView.as_view(),name='login'),
    path('logout/',CustomerLogoutView.as_view(),name='logout'),
    path('is-authenticated/',CheckCustomerIsAuthenticatedView.as_view(),name='is-authenticated')
]
