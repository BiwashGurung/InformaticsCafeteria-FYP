from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('login/',views.cafeteria_admin_login,name='cafeteria_admin_login'),
    path('dashboard/',views.cafeteria_admin_dashboard,name='cafeteria_admin_dashboard'),
]
