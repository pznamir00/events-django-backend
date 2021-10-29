from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('users.urls')),
    path('api/core/', include('core.urls')),
    path('api/tickets/', include('tickets.urls')),
    path('admin/', admin.site.urls),
]
