from django.contrib import admin
from django.urls import path
from .import views
from .views import admin_upload_popup, show_popup, view_event_history, manage_users, edit_user, delete_user, update_user_password

urlpatterns = [
    path('', show_popup, name='show_popup'),
    path('admin_login/',views.cafeteria_admin_login,name='cafeteria_admin_login'),
    path('dashboard/',views.cafeteria_admin_dashboard,name='cafeteria_admin_dashboard'),
    path('admin_logout/',views.logout_admin,name='logout_admin'),
    path('upload-popup/', admin_upload_popup, name='admin_upload_popup'),
    path('view-event-history/', views.view_event_history, name='view_event_history'),
    path('manage_users/', manage_users, name='manage_users'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('update-password/<int:user_id>/', update_user_password, name='update_user_password'),

]
