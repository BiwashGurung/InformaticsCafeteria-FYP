from django.contrib import admin
from django.urls import path
from .import views
from .views import admin_upload_popup, show_popup, manage_users, edit_user, delete_user, update_user_password, manage_menu, add_food_item , edit_food_item, delete_food_item, manage_orders, update_order_status, delete_order , manage_lost_found



urlpatterns = [
    path('', show_popup, name='show_popup'),
    path('admin_login/',views.cafeteria_admin_login,name='cafeteria_admin_login'),
    path('dashboard/',views.cafeteria_admin_dashboard,name='cafeteria_admin_dashboard'),
    path('admin_logout/',views.logout_admin,name='logout_admin'),
    path('upload-popup/', admin_upload_popup, name='admin_upload_popup'),
    path('view-event-history/', views.view_event_history, name='view_event_history'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('manage_users/', manage_users, name='manage_users'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('update-password/<int:user_id>/', update_user_password, name='update_user_password'),
    path('manage-menu/', manage_menu, name='manage_menu'),
    path('add-food/', add_food_item, name='add_food_item'),
    path('edit-food/<int:food_id>/', edit_food_item, name='edit_food_item'),
    path('delete-food/<int:food_id>/', delete_food_item, name='delete_food_item'),
    path('orders/', manage_orders, name='manage_orders'),
    path('orders/update/<int:order_id>/', update_order_status, name='update_order_status'),
    path('orders/delete/<int:order_id>/', delete_order, name='delete_order'),
    path('manage_lost_found/', manage_lost_found, name='manage_lost_found'),

]
  
  