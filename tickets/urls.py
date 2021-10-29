from django.urls import path
from . import views

urlpatterns = [
    path('events/<str:event_id>/tickets/<str:ticket_id>/', views.TicketAPIView.as_view())
]
