from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  
from cafeteria import views
from cafeteria_admin.views import show_popup
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cafeteria_admin/', include('cafeteria_admin.urls')),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('', show_popup, name='show_popup'),
    path('', show_popup, name='home'),
    path('college/', views.CollegePage, name='college'),
    path('aboutus/', views.AboutUsPage, name='aboutus'),
    path('contactus/', views.ContactUsPage, name='contactus'),
    path('logout/', views.LogoutPage, name='logout'),
    path('order_online/', views.OrderOnline, name='orderonline'),
    
    # Password reset views
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
