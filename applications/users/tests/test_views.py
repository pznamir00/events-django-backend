from unittest.mock import MagicMock, patch
import pytest
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from applications.core.models import Event
from applications.tickets.models import Ticket, TicketTemplate
from applications.users.models import User
from mixer.backend.django import mixer

from applications.users.views import UserAPIView


@pytest.mark.django_db
class TestUserAPIView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(
            username="testuser", password="password", email="test@gmail.com"
        )
        self.client = APIClient()

    def test_get_throws_an_401_if_user_is_not_auth(self):
        request = APIRequestFactory().get("")
        view = UserAPIView.as_view()
        response = view(request)
        assert response.status_code == 401

    def test_get_returns_logged_user(self):
        request = APIRequestFactory().get("")
        force_authenticate(request, user=self.user)
        view = UserAPIView.as_view()
        response = view(request)
        assert response.status_code == 200
        assert response.data["email"] == "test@gmail.com"  # type: ignore
