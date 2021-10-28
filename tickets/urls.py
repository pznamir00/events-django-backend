from django.urls import path
from . import views

urlpatterns = [
    path('events/<str:event_id>/tickets/', views.TicketAPIView.as_view())
]
