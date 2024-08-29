from django.urls import reverse, resolve
import pytest
from .. import views


@pytest.mark.urls("applications.tickets.urls")
class TestTicketsUrls:
    def test_event_tickets_url_resolves(self):
        url = reverse("events-tickets", args=["event123"])
        assert resolve(url).func.view_class == views.TicketAPIView  # type: ignore

    def test_event_tickets_checker_url_resolves(self):
        url = reverse("events-tickets-checker", args=["event123", "ticket123"])
        assert resolve(url).func.view_class == views.TicketCheckerAPIView  # type: ignore
