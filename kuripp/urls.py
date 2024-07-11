from django.contrib import admin
from django.urls import path, include
from core import views  # Import views from the core app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),  # Include the core app's URLs
]