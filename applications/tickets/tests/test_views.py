from unittest.mock import MagicMock, patch
import pytest
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from applications.core.models import Event
from applications.tickets.models import Ticket, TicketTemplate
from applications.tickets.views import TicketAPIView, TicketCheckerAPIView
from applications.users.models import User
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestTicketCheckerAPIView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = APIClient()

    @pytest.fixture
    def entities(self):
        event: Event = mixer.blend("core.Event")

        template: TicketTemplate = mixer.blend("tickets.TicketTemplate")
        template.event = event
        template.save()

        ticket: Ticket = mixer.blend("tickets.Ticket")
        ticket.template = template
        ticket.is_sold = True
        ticket.is_used = False
        ticket.save()

        return {"event": event, "template": template, "ticket": ticket}

    def test_get_throws_an_401_if_user_is_not_auth(self):
        request = APIRequestFactory().get("")
        view = TicketCheckerAPIView.as_view()
        response = view(request, event_id=4, ticket_id=7)
        assert response.status_code == 401

    def test_get_throws_404_if_object_does_not_exist(self):
        request = APIRequestFactory().get("")
        force_authenticate(request, user=self.user)
        view = TicketCheckerAPIView.as_view()
        response = view(request, event_id=4, ticket_id=7)
        assert response.status_code == 404

    def test_get_returns_correct_data(self, entities: dict):
        request = APIRequestFactory().get("")
        force_authenticate(request, user=self.user)
        view = TicketCheckerAPIView.as_view()
        event, ticket = entities["event"], entities["ticket"]
        response = view(request, event_id=event.id, ticket_id=ticket.id)
        assert response.status_code == 200
        assert response.data == {  # type: ignore
            "is_used": True,
            "is_sold": True,
            "id": str(ticket.id),
        }


@pytest.mark.django_db
class TestTicketAPIView:
    ticket_sender_cls = MagicMock()
    sender_mock: MagicMock

    @pytest.fixture(autouse=True)
    def setup(self):
        self.sender_mock = MagicMock()
        ticket_sender_cls: MagicMock = self.ticket_sender_cls
        ticket_sender_cls.return_value = self.sender_mock

    @pytest.fixture
    def entities(self):
        event: Event = mixer.blend("core.Event")
        event.is_free = False
        event.save()

        template: TicketTemplate = mixer.blend("tickets.TicketTemplate")
        template.event = event
        template.save()

        ticket: Ticket = mixer.blend("tickets.Ticket")
        ticket.template = template
        ticket.is_sold = False
        ticket.is_used = False
        ticket.save()

        return {"event": event, "template": template, "ticket": ticket}

    def test_post_returns_404_if_event_does_not_exist(self):
        request = APIRequestFactory().post("")
        view = TicketAPIView.as_view()
        response = view(request, event_id=4)
        assert response.status_code == 404

    def test_post_returns_404_if_event_exists_but_is_free(self, entities: dict):
        event = entities["event"]
        event.is_free = True
        event.save()
        request = APIRequestFactory().post("")
        view = TicketAPIView.as_view()
        response = view(request, event_id=event.id)
        assert response.status_code == 404

    def test_post_throws_error_if_email_is_missing(self, entities: dict):
        event = entities["event"]
        request = APIRequestFactory().post("", {})
        view = TicketAPIView.as_view()
        response = view(request, event_id=event.id)
        assert response.status_code == 400

    def test_post_throws_error_if_email_has_wrong_format(self, entities: dict):
        event = entities["event"]
        request = APIRequestFactory().post("", {"email": "ppp"})
        view = TicketAPIView.as_view()
        response = view(request, event_id=event.id)
        assert response.status_code == 400

    @patch("applications.tickets.views.TicketWithQRCodeSender", ticket_sender_cls)
    def test_post_returns_200_if_request_is_valid(self, entities: dict):
        event = entities["event"]
        request = APIRequestFactory().post("", {"email": "test@gmail.com"})
        view = TicketAPIView.as_view()
        response = view(request, event_id=event.id)
        assert response.status_code == 200

    @patch("applications.tickets.views.TicketWithQRCodeSender", ticket_sender_cls)
    def test_post_calls_sender_send_if_request_is_valid(self, entities: dict):
        event, ticket = entities["event"], entities["ticket"]
        request = APIRequestFactory().post("", {"email": "test@gmail.com"})
        view = TicketAPIView.as_view()
        view(request, event_id=event.id)
        send: MagicMock = self.sender_mock.send
        send.assert_called_with("test@gmail.com", ticket)

    @patch("applications.tickets.views.TicketWithQRCodeSender", ticket_sender_cls)
    def test_post_passes_if_user_is_auth_and_email_is_missing(self, entities: dict):
        event, ticket = entities["event"], entities["ticket"]
        request = APIRequestFactory().post("")
        user = User.objects.create_user(
            username="testuser", password="password", email="newuser@gmail.com"
        )
        force_authenticate(request, user=user)
        view = TicketAPIView.as_view()
        view(request, event_id=event.id)
        send: MagicMock = self.sender_mock.send
        send.assert_called_with("newuser@gmail.com", ticket)
