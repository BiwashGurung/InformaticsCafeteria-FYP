from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def cafeteria_admin_dashboard(request):
    return HttpResponse("This is the cafeteria admin dashboard")

def cafeteria_admin_login(request):
   if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       if username == 'informatics' and password == 'informatics@123':
           return HttpResponse("Login successful")
       else:
           return HttpResponse("Login failed")