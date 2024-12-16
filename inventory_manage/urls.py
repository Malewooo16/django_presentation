from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),              # Admin interface
    path('inventory/', include('inventory.urls')),  # Routes for inventory app
    path('', include('inventory.urls')),          # Redirect root to inventory
]
