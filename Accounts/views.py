from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from Accounts.models import User, Customer, Seller, UserOTP
from django.contrib import messages

# For Authentication-------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# For OTP Creation---------------------------------------------------
import random

# For Mail Sending -------------------------------------------------
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def home(request):
    user = request.user
    data = {
        'user':user,
    }
    return render(request, 'home.html', data)

def customer_reg(request):
    if request.method == "POST":
        First_Name = request.POST["first_name"]
        Last_Name = request.POST["last_name"]
        Email_Address = request.POST["email"]
        Phone_Number = request.POST["phone"]
        password = request.POST["password"]
        Confirm_Password = request.POST["c_password"]

        # print("--------------------------------------------")
        # print("Customer Account")
        # print(f"First Name:{First_Name}, Last Name: {Last_Name}, Email: {Email_Address}, Password: {password}, Confirm Password: {Confirm_Password}")
        # print("--------------------------------------------")

        if password == Confirm_Password:
            if User.objects.filter(email=Email_Address).exists():
                messages.error(request, 'This email is already taken.')
                return redirect(customer_reg)
            else:
                user_obj = User.objects.create(first_name=First_Name, last_name=Last_Name, email=Email_Address, mobile = Phone_Number, password=password, is_customer=True)
                user_obj.set_password(password)
                user_obj.is_active = False
                user_obj.save()
                # It Replace Signals---------------------------
                customer= Customer.objects.create(user=user_obj)
                customer.save()

                # Now Send Mail-------------------------------------------
                usr_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user = user_obj, otp = usr_otp)

                mess = f"Hello {user_obj.first_name}{user_obj.last_name},\nYour OTP is {usr_otp}\nThanks!"

                send_mail(
                    "Welcome to IT-MrH Solution - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user_obj.email],
                    fail_silently = False
                    )
                return render(request, 'Accounts/OTP_verify.html', {'user': user_obj})

    return render(request, 'Accounts/c_registration.html')




def seller_reg(request):
    if request.method == "POST":
        First_Name = request.POST["first_name"]
        Last_Name = request.POST["last_name"]
        Email_Address = request.POST["email"]
        Phone_Number = request.POST["phone"]
        password = request.POST["password"]
        Confirm_Password = request.POST["c_password"]

        # print("--------------------------------------------")
        # print("Seller Account")
        # print(f"First Name:{First_Name}, Last Name: {Last_Name}, Email: {Email_Address}, Password: {password}, Confirm Password: {Confirm_Password}")
        # print("--------------------------------------------")

        if password == Confirm_Password:
            if User.objects.filter(email=Email_Address).exists():
                messages.error(request, 'This email is already taken.')
                return redirect(seller_reg)
            else:
                user_obj = User.objects.create(first_name=First_Name, last_name=Last_Name, email=Email_Address, mobile = Phone_Number, password=password, is_seller=True)
                user_obj.set_password(password)
                user_obj.is_active = False
                user_obj.save()
                # It Replace Signals---------------------------
                seller= Seller.objects.create(user=user_obj)
                seller.save()
                # Now Send Mail-------------------------------------------
                usr_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user = user_obj, otp = usr_otp)

                mess = f"Hello {user_obj.first_name}{user_obj.last_name},\nYour OTP is {usr_otp}\nThanks!"

                send_mail(
                    "Welcome to IT-MrH Solution - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user_obj.email],
                    fail_silently = False
                    )
                return render(request, 'Accounts/OTP_verify.html', {'user': user_obj})
            
    return render(request, 'Accounts/s_registration.html')






def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # print("--------------------------------------------")
        # print(f"Email: {email}, Password: {password}")
        # print("--------------------------------------------")

        user_obj = User.objects.filter(email=email).first()
        user_a = User.objects.filter(email = email).exists()
        if user_obj is not None:
            # Customer Login-----------------------------------------------------------------------------------------
            if user_obj.is_customer == True and user_obj.is_active == True:
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('user_profile')
            elif user_obj.is_customer == True and user_obj.is_active == False:
                usr = User.objects.filter(email=email).first()
                UserOTP.objects.get(user = usr).delete()
                usr_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user = usr, otp = usr_otp)
                mess = f"Hello {usr.first_name}{usr.last_name},\nYour OTP is {usr_otp}\nThanks!"

                send_mail(
                    "Welcome to IT-MrH Solution - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently = False
                    )
                return render(request, 'Accounts/OTP_verify.html', {'user': usr})
            # Seller Login------------------------------------------------------------------------------------------
            elif user_obj.is_seller == True and user_obj.is_active == True:
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('seller_profile')
            elif user_obj.is_seller == True and user_obj.is_active == False:
                usr = User.objects.filter(email=email).first()
                UserOTP.objects.get(user = usr).delete()
                usr_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user = usr, otp = usr_otp)
                mess = f"Hello {usr.first_name}{usr.last_name},\nYour OTP is {usr_otp}\nThanks!"

                send_mail(
                    "Welcome to IT-MrH Solution - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently = False
                    )
                return render(request, 'Accounts/OTP_verify.html', {'user': usr})
        elif not User.objects.filter(email = email).exists():
            messages.warning(request, f'Please enter a correct email and password. Note that both fields may be case-sensitive.')
            return redirect('user_login')
        
    return render(request, 'Accounts/login.html')





@login_required
def user_profile(request):
    user = request.user
    data = {
        'user': user
    }
    return render(request, 'Accounts/user_profile.html', data)

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')






@login_required
def seller_profile(request):
    user = request.user
    data = {
        'user': user
    }
    return render(request, 'SellerProfile/seller_profile.html', data)






def otp_verify(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp') #213243 #None

        if get_otp:
            get_usr = request.POST.get('user_otp')
            user_obj = User.objects.get(email=get_usr)
            if user_obj:
                if user_obj.is_customer == True and user_obj.is_active == False:
                    user = user_obj  # Or users[0]
                    otp_obj = UserOTP.objects.get(user = user)
                    given_otp = int(get_otp)
                    correct_otp = otp_obj.otp
                    # print("-----------------------")
                    # print('Given OTP =', given_otp)
                    # print("User =",user)
                    # print("Correct OTP =",correct_otp)
                    # print("-----------------------")
                    if given_otp == correct_otp:
                        user.is_active = True
                        user.save()
                        messages.success(request, f'Account is Successfully Created. Now {user.first_name}{user.last_name} you can login.')
                        return redirect('user_login')
                    else:
                        messages.warning(request, f'You Entered a Wrong OTP')
                        return render(request, 'Accounts/OTP_verify.html', {'user': user})
                
                elif user_obj.is_seller == True and user_obj.is_active == False:
                    user = user_obj  # Or users[0]
                    otp_obj = UserOTP.objects.get(user = user)
                    given_otp = int(get_otp)
                    correct_otp = otp_obj.otp
                    # print("-----------------------")
                    # print('Given OTP =', given_otp)
                    # print("User =",user)
                    # print("Correct OTP =",correct_otp)
                    # print("-----------------------")
                    if given_otp == correct_otp:
                        user.save()
                        messages.success(request, f'{user.first_name}{user.last_name} Your Account is Successfully Created.')
                        return render(request, 'Accounts/s_registration_2.html', {'user':user})
                    else:
                        messages.warning(request, f'You Entered a Wrong OTP')
                        return render(request, 'Accounts/OTP_verify.html', {'user': user})
            else:
                messages.error(request, f'Your Email is Not Exist.')
                return redirect('home')
        
        
    return render(request, 'Accounts/OTP_verify.html')


## With Javascripts-----------------------------------------------------------------------------------------
# def resend_OTP(request):
#     if request.method == "GET":
#         get_usr = request.GET['user']
#         print("--------------------------")
#         print(get_usr)
#         print("--------------------------")
#     if User.objects.filter(email = get_usr).exists() and not User.objects.get(email = get_usr).is_active:
#         usr = User.objects.get(email=get_usr)
#         UserOTP.objects.get(user = usr).delete()
#         usr_otp = random.randint(100000, 999999)
#         UserOTP.objects.create(user = usr, otp = usr_otp)
#         mess = f"Hello {usr.first_name}{usr.last_name},\nYour OTP is {usr_otp}\nThanks!"

#         send_mail(
#             "Welcome to IT-MrH Solution - Verify Your Email",
#             mess,
#             settings.EMAIL_HOST_USER,
#             [usr.email],
#             fail_silently = False
#             )
#         return JsonResponse('Sending OTP Sccessfully.')
#     return JsonResponse('We face some tecnical problem.')

## Withot Javascripts----------------------------------------------------------------------------------------
def resend_OTP(request):
    if request.method == "GET":
        get_usr = request.GET.get('otp')
        # print("--------------------------")
        # print("User Email: ",get_usr)
        # print("--------------------------")
        usr = User.objects.filter(email=get_usr).first()
        if User.objects.filter(email = get_usr).exists() and not User.objects.get(email = get_usr).is_active:
            usr = User.objects.get(email=get_usr)
            UserOTP.objects.get(user = usr).delete()
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user = usr, otp = usr_otp)
            mess = f"Hello {usr.first_name}{usr.last_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to IT-MrH Solution - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently = False
                )
            return render(request, 'Accounts/OTP_verify.html', {'user': usr})
        
        return render(request, 'Accounts/OTP_verify.html', {'user': usr})



def seller_info(request):
    if request.method == "POST":
        usr_email = request.POST.get('user')
        shop_name = request.POST.get('shop_name')
        tread_licence = request.FILES.get('tread_licence')
        nid = request.FILES.get('nid')
        # print('-----------------------------')
        # print(usr_email,shop_name,tread_licence,nid)
        # print('-----------------------------')
        usr = User.objects.get(email = usr_email)
        seller = Seller.objects.get(user = usr)
        if seller:
            # seller.objects.create(shope_name = shop_name,Trade_license = tread_licence, Owner_NID = nid)
            seller.shope_name = shop_name
            seller.Trade_license = tread_licence
            seller.Owner_NID = nid
            seller.save()
            mess = f"Hello {usr.first_name}{usr.last_name},\nPlease wait patiently, we will verify your information and activate your account. Thank you."
            send_mail(
                "Welcome to IT-MrH Solution - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently = False
                )
            return redirect('home')

    return render(request, "Accounts/s_registration_2.html")