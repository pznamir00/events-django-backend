import pytest
from applications.core.validators import CheckIfTicketProvidedIfPrivate
from rest_framework.serializers import ValidationError


class TestCheckIfTicketProvidedIfPrivate:
    def test_throws_error_if_event_is_not_free_and_ticket_is_missing(self):
        validator = CheckIfTicketProvidedIfPrivate()
        with pytest.raises(ValidationError):
            validator({"is_free": False})
            raise Exception("Error should have been thrown")

    def test_passes_if_is_free_is_not_provided(self):
        validator = CheckIfTicketProvidedIfPrivate()
        validator({})

    def test_passes_if_event_is_not_free_but_ticket_is_provided(self):
        validator = CheckIfTicketProvidedIfPrivate()
        validator({"is_free": False, "ticket": {}})
