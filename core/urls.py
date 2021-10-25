from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('followed-hashtags', views.FollowedHashTagView, basename='followedHashtags')
router.register('events', views.EventViewSet, basename='events')

urlpatterns = [
    path('/', include(router.urls)),
    path('events-own-list/', views.EventOwnListView.as_view())
]
