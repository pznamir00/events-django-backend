import pytest
from applications.tickets.models import Ticket
from applications.tickets.serializers import (
    TicketPurchaseSerializer,
    TicketSerializer,
)
from mixer.backend.django import mixer


class TestTicketPurchaseSerializer:
    def test_validation_passes_if_email_is_provided(self):
        instance = TicketPurchaseSerializer(data={"email": "test@gamil.com"})
        assert instance.is_valid()

    def test_validation_does_not_pass_if_email_is_missing(self):
        instance = TicketPurchaseSerializer(data={})
        assert not instance.is_valid()

    def test_validation_does_not_pass_if_email_is_not_valid_email(self):
        instance = TicketPurchaseSerializer(data={"email": "aaa"})
        assert not instance.is_valid()


class TestTicketSerializer:
    def test_validation_passes_if_data_is_valid(self):
        instance = TicketSerializer(data={"is_used": True, "is_sold": True})
        assert instance.is_valid()

    @pytest.mark.django_db
    def test_returns_object_without_template(self):
        ticket: Ticket = mixer.blend("tickets.Ticket")
        instance = TicketSerializer(instance=ticket)
        assert "template" not in instance.data
