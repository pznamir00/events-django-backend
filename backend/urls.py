from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/auth/", include("applications.users.urls")),
    path("api/core/", include("applications.core.urls")),
    path("api/tickets/", include("applications.tickets.urls")),
    path("admin/", admin.site.urls),
]
