from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('admin/', admin.site.urls),              # Admin interface
    path('inventory/', include('inventory.urls')),  # Routes for inventory app  
    path('store/', include('store_management.urls')),     # Redirect root to inventory
]
