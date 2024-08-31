from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(
    "followed-hashtags", views.FollowedHashTagView, basename="followed-hashtags"
)
router.register("events", views.EventViewSet, basename="events")
router.register("own-events", views.EventOwnListViewSet, basename="own-events")

urlpatterns = [path("", include(router.urls))]
