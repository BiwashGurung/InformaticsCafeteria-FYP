from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views  
from cafeteria import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('', views.HomePage, name='home'),
    path('college/', views.CollegePage, name='college'),
    path('aboutus/', views.AboutUsPage, name='aboutus'),
    path('contactus/', views.ContactUsPage, name='contactus'),
    path('logout/', views.LogoutPage, name='logout'),
    
    # Password reset views
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
