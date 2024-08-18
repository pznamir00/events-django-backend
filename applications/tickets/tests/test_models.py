import uuid
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestTicketsModels:
    def test_create_ticket_template(self):
        entity = mixer.blend("tickets.TicketTemplate")
        assert entity.pk == 1, "Should create a TicketTemplate instance"

    def test_fail_ticket_template_if_file_is_not_pdf(self):
        with pytest.raises(ValidationError):
            entity = mixer.blend("tickets.TicketTemplate")
            entity._file = SimpleUploadedFile("test_file.txt", b"file_content")
            entity.full_clean()
            raise Exception("Error should have been thrown")

    def test_create_ticket(self):
        entity = mixer.blend("tickets.Ticket")
        assert isinstance(entity.id, uuid.UUID), "Should create a Ticket instance"
