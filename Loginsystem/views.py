from django.shortcuts import render,redirect
import smtplib
from django.contrib import messages
import random
from email.message import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import ssl
from .models import OTP_Data

def Loginpage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username = email,password = password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are Logged in successfully")
            return redirect("/")
        else:
            messages.warning(request,"Please Enter Valid username and Password")
            return redirect("/login/")
    return render(request,'Loginsystem/login.html')

def Signuppage(request):
    enable_otp = 0

    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        m_number = request.POST.get("mnumber")
        OTP_Data.objects.all().delete()
        if User.objects.filter(username=email).exists():
            messages.warning(request,"This user is already exist")
        else:
            otp_generate = random.randrange(1000, 9999)
            OTP_data = OTP_Data(email_id = email,otp = otp_generate)
            OTP_data.save()
    
            email_sender = 'rotomouldingmaker@gmail.com'
    
            email_password = 'emwklaggpqvjwlwu'
            email_receiver = email
    
            subject = "OTP"
            body = """
            Welcome to ROTO MOLDING 
            Your OTP is - {}""".format(otp_generate)
            em = EmailMessage()
            em['from'] = email_sender
            em['to'] = email_receiver
            em['subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
    
            with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
            enable_otp = 1
    return render(request,"Loginsystem/signup.html",{"enable_otp":enable_otp})

def PasswordPage(request):
    local_data = 0
    if request.method == "POST":
        email = request.POST.get("mailid")
        otp = request.POST.get("otp")
        mydata = OTP_Data.objects.filter(email_id=email).values()
        otp_field = str(mydata)[-7:-3]
        print(email)
        print(otp_field)
        if otp == otp_field:
            otp_data = OTP_Data.objects.filter(email_id = email)
            otp_data.delete()
            local_data = 1
            return render(request,"Loginsystem/password.html",{"local_data":local_data})
        else:
            enable_otp = 1
            messages.warning(request,"Please Enter Valid OTP")
            return render(request,"Loginsystem/signup.html",{"enable_otp":enable_otp})
    return render(request,"Loginsystem/password.html")


def ForgetPage(request):
    enable_otp = 0
    if request.method == "POST":
        email = request.POST.get("email")
        OTP_Data.objects.all().delete()
        user = User.objects.filter(username = email)
        if user is not None:
            otp_generate = random.randrange(1000, 9999)
            OTP_data = OTP_Data(email_id = email,otp = otp_generate)
            OTP_data.save()
            email_sender = 'rotomouldingmaker@gmail.com'
            email_password = 'emwklaggpqvjwlwu'
            email_receiver = email
            subject = "OTP"
            body = """
            Welcome to ROTO MOLDING 
            Your OTP is - {}""".format(otp_generate)
            em = EmailMessage()
            em['from'] = email_sender
            em['to'] = email_receiver
            em['subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
            enable_otp = 1
            return render(request,'Loginsystem/forget.html',{"enable_otp":enable_otp})
        else:
            messages.warning(request,"Please Enter Valid email")
    return render(request,'Loginsystem/forget.html')

def ChangePassPage(request):
    if request.method == "POST":
        email = request.POST.get("mail_id")
        otp = request.POST.get("otp")
        mydata = OTP_Data.objects.filter(email_id=email).values()
        otp_field = str(mydata)[-7:-3]
        print(email)
        print(mydata)
        print(otp_field)
        if otp == otp_field:
            otp_data = OTP_Data.objects.filter(email_id = email)
            otp_data.delete()
            local_data = 1
            return render(request,"Loginsystem/change_pass.html",{"local_data":local_data})
        else:
            enable_otp = 1
            messages.warning(request,"Please Enter Valid OTP")
            return render(request,"Loginsystem/forget.html",{"enable_otp":enable_otp})
    return render(request,'Loginsystem/forget.html')


def new_pass(request):
    if request.method == "POST":
        email = request.POST.get("mail_id")
        password = request.POST.get("pass")
        cpassword = request.POST.get("cpass")
        if password == cpassword:
            user = User.objects.get(username = email)
            user.set_password(password)
            user.save()
            messages.success(request,"Your password has been changed")
            return redirect("/")
        else:
            messages.warning(request,"Doesn't match password")
            return render(request,"Loginsystem/change_pass.html")
    return redirect("/")