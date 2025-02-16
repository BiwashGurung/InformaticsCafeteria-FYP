from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import EventPopup
from .forms import EventPopupForm
from datetime import datetime

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
