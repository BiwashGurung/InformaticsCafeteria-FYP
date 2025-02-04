from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import admin_upload_popup, show_popup

urlpatterns = [
    path('admin_login/',views.cafeteria_admin_login,name='cafeteria_admin_login'),
    path('dashboard/',views.cafeteria_admin_dashboard,name='cafeteria_admin_dashboard'),
     path('admin_logout/',views.logout_admin,name='logout_admin'),
     path('upload-popup/', admin_upload_popup, name='admin_upload_popup'),
    path('', show_popup, name='show_popup'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
