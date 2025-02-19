from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import EventPopup
from .forms import EventPopupForm
from datetime import datetime
# Importing Profile from cafeteria app
from cafeteria.models import Profile  
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin, login_url='/cafeteria_admin/admin_login/')
def cafeteria_admin_dashboard(request):
    return render(request, 'cafeteria_admin/dashboard.html')


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
                messages.error(request, 'You are not authorized to access admin panel.')
        else:
            messages.error(request, 'Invalid admin username or password.')
    return render(request, 'cafeteria_admin/admin_login.html')

def logout_admin(request):

    return redirect('/cafeteria_admin/admin_login/')


def admin_upload_popup(request):
    if request.method == 'POST':
        form = EventPopupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_upload_popup')  
    else:
        form = EventPopupForm()

    return render(request, 'cafeteria_admin/event_popup.html', {'form': form})

def show_popup(request):
    current_time = datetime.now()
    event = EventPopup.objects.filter(start_date__lte=current_time, end_date__gte=current_time).order_by('-start_date').first()  
    return render(request, 'cafeteria/index.html', {'event': event})

def view_event_history(request):
    #Fetching all events
    events = EventPopup.objects.all() 
    return render(request, 'cafeteria_admin/view_event_history.html', {'events': events})


    



@user_passes_test(is_admin, login_url='/cafeteria_admin/admin_login/')
def manage_users(request):
    # Fetching all users
    users = Profile.objects.all()  
    return render(request, 'cafeteria_admin/manage_users.html', {'users': users})

@user_passes_test(is_admin, login_url='/cafeteria_admin/admin_login/')
def edit_user(request, user_id):
    user = get_object_or_404(Profile, id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.phone = request.POST['phone']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('manage_users')
    return render(request, 'cafeteria_admin/edit_user.html', {'user': user})

@user_passes_test(is_admin, login_url='/cafeteria_admin/admin_login/')
def delete_user(request, user_id):
    user = get_object_or_404(Profile, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('manage_users')

def update_user_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('manage_users')

        user.password = make_password(new_password)
        user.save()
        messages.success(request, f"Password for {user.username} updated successfully.")
        return redirect('manage_users')

    return render(request, 'cafeteria_admin/update_password.html', {'user': user})    


  
