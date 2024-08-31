import uuid
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer
from ..models import TicketTemplate


@pytest.mark.django_db
class TestTicketTemplate:
    def test_create_ticket_template(self):
        entity = mixer.blend("tickets.TicketTemplate")
        assert isinstance(entity, TicketTemplate)

    def test_fail_ticket_template_if_file_is_not_pdf(self):
        with pytest.raises(ValidationError):
            entity = mixer.blend("tickets.TicketTemplate")
            entity.file = SimpleUploadedFile("test_file.txt", b"file_content")  # type: ignore
            entity.full_clean()  # type: ignore
            raise Exception("Error should have been thrown")


@pytest.mark.django_db
class TestTicket:
    def test_create_ticket(self):
        entity = mixer.blend("tickets.Ticket")
        assert isinstance(entity.id, uuid.UUID), "Should create a Ticket instance"  # type: ignore
