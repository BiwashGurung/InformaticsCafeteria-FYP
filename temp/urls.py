from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  
from cafeteria import views
from cafeteria_admin.views import show_popup
from django.conf import settings
from django.conf.urls.static import static
from cafeteria.views import food_list, view_cart, add_to_cart, update_cart, remove_from_cart, clear_cart,cart_summary, place_order, order_history , initkhalti , khalti_callback , lost_found_page , profile_page


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
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('profile/', profile_page, name='profile'),

    # Khalti
    path('initiate/', initkhalti, name='initiate'),
    path('khalti-callback/', khalti_callback, name='khalti_callback'),


    # Lost and Found
    path('lost-found/', lost_found_page, name='lost_found_page'),

    # Group Order 
    path('group-order/', views.group_order_page, name='group_order_page'),
    path('group-order/<str:group_code>/', views.group_order_detail, name='group_order_detail'),

    #Feedback
    path('feedback/', views.feedback_page, name='feedback_page'),
    path('delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('add_reply/<int:feedback_id>/', views.add_reply, name='add_reply'),
    path('add_subreply/<int:reply_id>/', views.add_subreply, name='add_subreply'),
    path('edit_reply/<int:reply_id>/', views.edit_reply, name='edit_reply'),
    path('delete_reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('react/<int:feedback_id>/<str:reaction_type>/', views.react, name='react'),    
    
    # Password reset views
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.txt', 
        html_email_template_name='registration/password_reset_email.html',  
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name='registration/password_reset_confirm.html'
    # ), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='registration/password_reset_complete.html'
    # ), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
