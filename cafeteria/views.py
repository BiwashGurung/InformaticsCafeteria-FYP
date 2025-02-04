from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile


def HomePage(request):
    return render(request, 'cafeteria/index.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        user = User.objects.create_user(username=uname, email=email, password=password)
        Profile.objects.create(user=user,username=uname,email=email, phone=phone)
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'cafeteria/registration.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # Handling session expiration based on 'remember me'
            if remember_me:
                # 1 week session expiry
                request.session.set_expiry(604800)  
            else:
                # Session expires when the browser is closed
                request.session.set_expiry(0) 

            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'cafeteria/login.html')

def LogoutPage(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


def CollegePage(request):
    return render(request, 'cafeteria/college.html')    

def AboutUsPage(request):
    return render(request, 'cafeteria/aboutus.html')

def ContactUsPage(request):
    return render(request, 'cafeteria/contactus.html')

def OrderOnline(request):
    return render(request, 'cafeteria/orderonline.html')