from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def cafeteria_admin_dashboard(request):
    return HttpResponse("This is the cafeteria admin dashboard")