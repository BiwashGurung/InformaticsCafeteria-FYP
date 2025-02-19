from django.contrib import admin
from django.urls import path
from .import views
from .views import admin_upload_popup, show_popup, manage_users, edit_user, delete_user

urlpatterns = [
    path('', show_popup, name='show_popup'),
    path('admin_login/',views.cafeteria_admin_login,name='cafeteria_admin_login'),
    path('dashboard/',views.cafeteria_admin_dashboard,name='cafeteria_admin_dashboard'),
    path('admin_logout/',views.logout_admin,name='logout_admin'),
    path('upload-popup/', admin_upload_popup, name='admin_upload_popup'),
    path('manage_users/', manage_users, name='manage_users'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
]
