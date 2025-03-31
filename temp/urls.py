from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  
from cafeteria import views
from cafeteria_admin.views import show_popup
from django.conf import settings
from django.conf.urls.static import static
from cafeteria.views import food_list, view_cart, add_to_cart, update_cart, remove_from_cart, clear_cart,cart_summary, place_order, order_history , initkhalti , khalti_callback , lost_found_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cafeteria_admin/', include('cafeteria_admin.urls')),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    # path('', show_popup, name='show_popup'),
    path('', show_popup, name='home'),
    path('college/', views.CollegePage, name='college'),
    path('aboutus/', views.AboutUsPage, name='aboutus'),
    path('contactus/', views.ContactUsPage, name='contactus'),
    path('logout/', views.LogoutPage, name='logout'),
    path('order_online/', views.OrderOnline, name='orderonline'),
    path('menu/<str:category>/', food_list, name='food_list'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),

    path('cartsummary/', cart_summary, name='cartsummary'),
    path('checkout/', place_order, name='place_order'),
    path('orders/', order_history, name='order_history'),


    # Khalti
    path('initiate/', initkhalti, name='initiate'),
    path('khalti-callback/', khalti_callback, name='khalti_callback'),


    # Lost and Found
    path('lost-found/', lost_found_page, name='lost_found_page'),

    # Group Order 
    path('group-order/', views.group_order_page, name='group_order_page'),
    path('group-order/<str:group_code>/', views.group_order_detail, name='group_order_detail'),
    
    # Password reset views
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
