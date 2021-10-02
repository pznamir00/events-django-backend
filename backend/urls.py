from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('users.urls')),
    path('core/', include('core.urls')),
    path('drivers/', include('drivers.urls')),
    path('admin/', admin.site.urls),
]
