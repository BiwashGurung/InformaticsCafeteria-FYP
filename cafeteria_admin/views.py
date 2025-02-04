from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def is_admin(user):
    return user.is_staff


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='/cafeteria_admin/login/')
def cafeteria_admin_dashboard(request):
    return HttpResponse("This is the cafeteria admin dashboard")


def cafeteria_admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('/cafeteria_admin/dashboard/')
            else:
                messages.error(request, 'You are not authorized to access this page.')
        else:
            messages.error(request, 'Invalid admin username or password.')
    return render(request, 'cafeteria_admin/admin_login.html')