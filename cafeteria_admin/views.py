from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

# Create your views here.
def cafeteria_admin_dashboard(request):
    return HttpResponse("This is the cafeteria admin dashboard")

def cafeteria_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('cafeteria_admin_dashboard')
    return render(request, 'cafeteria_admin/admin_login.html')