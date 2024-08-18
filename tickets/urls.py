from django.urls import path
from . import views

urlpatterns = [
    path(
        "events/<str:event_id>/tickets/",
        views.TicketAPIView.as_view(),
        name="events-tickets",
    ),
    path(
        "events/<str:event_id>/tickets/<str:ticket_id>/",
        views.TicketCheckerAPIView.as_view(),
        name="events-tickets-checker",
    ),
]
