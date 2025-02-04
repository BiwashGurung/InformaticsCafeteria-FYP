from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('dashboard/',views.cafeteria_admin_dashboard,name='cafeteria_admin_dashboard'),
    path('login/',views.cafeteria_admin_login,name='cafeteria_admin_login'),
]
