from django.urls import path
from .views import *

app_name = 'customer'

urlpatterns = [
    path('signup/', CustomerSignupView.as_view(), name='signup'),
    path('login/', CustomerLoginView.as_view(), name='login'),
]
