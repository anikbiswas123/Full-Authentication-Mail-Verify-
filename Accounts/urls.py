from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('customer_reg/', customer_reg, name='customer_reg'),
    path('seller_reg/', seller_reg, name='seller_reg'),
    path('seller_info/', seller_info, name='seller_info'),


    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    
    path('user_profile/', user_profile, name='user_profile'),
    path('seller_profile/', seller_profile, name='seller_profile'),



    path('otp_verify/', otp_verify, name='otp_verify'),
    path('resend_OTP/', resend_OTP, name='resend_OTP'),
]
