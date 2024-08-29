from django.urls import path, include
from . import views


urlpatterns = [
    path("user/", views.UserAPIView.as_view(), name="user"),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("password/", include("django.contrib.auth.urls")),
    path("", include("dj_rest_auth.urls")),
]
