import os
from typing import cast
from unittest.mock import MagicMock, patch
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from applications.tickets.tests.utils import load_mock_image, load_mock_pdf
from ..models import TicketTemplate, Ticket
import applications.tickets.helpers as helpers
from applications.core.models import Event
from mixer.backend.django import mixer


class TestTicketGenerator:
    def test_should_generate_tickets_returns_true_if_event_is_not_free(self):
        generator = helpers.TicketGenerator({"is_free": False})
        assert generator.should_generate_tickets()

    def test_should_generate_tickets_returns_false_if_event_is_free(self):
        generator = helpers.TicketGenerator({"is_free": True})
        assert not generator.should_generate_tickets()

    @pytest.mark.django_db
    def test_generate_tickets_creates_ticket_template(self):
        template = SimpleUploadedFile("test_file.pdf", b"file_content")
        event: Event = mixer.blend("core.Event")
        generator = helpers.TicketGenerator({})
        generator.generate_tickets({"template": template, "quantity": 2}, event)
        obj = TicketTemplate.objects.latest("id")
        assert obj._file.name.startswith("media/tickets/test_file")

    @pytest.mark.django_db
    def test_generate_tickets_creates_tickets(self):
        template = SimpleUploadedFile("test_file.pdf", b"file_content")
        event: Event = mixer.blend("core.Event")
        generator = helpers.TicketGenerator({})
        generator.generate_tickets({"template": template, "quantity": 5}, event)
        assert Ticket.objects.count() == 5


class TestTicketWithQRCodeSender:
    email_mock = MagicMock()

    @pytest.fixture(autouse=True)
    def remove_tmp_files(self):
        files = [i for i in os.listdir("media/tmp/") if i != ".gitignore"]
        for file in files:
            os.unlink(f"media/tmp/{file}")

    @pytest.mark.django_db
    def test_send_does_not_leave_redundant_media_tmp_files(self):
        ticket: Ticket = mixer.blend("tickets.Ticket")
        ticket.template._file = load_mock_pdf()  # type:ignore
        sender = helpers.TicketWithQRCodeSender()
        sender.send("test@gmail.com", ticket)
        tmp_files = [i for i in os.listdir("media/tmp/") if i != ".gitignore"]
        assert not len(tmp_files)

    @pytest.mark.django_db
    @patch("applications.tickets.helpers.qrcode.make", return_value=load_mock_image())
    def test_send_calls_qr_make_with_correct_url(self, mock_make: MagicMock):
        ticket: Ticket = mixer.blend("tickets.Ticket")
        ticket.template._file = load_mock_pdf()  # type:ignore
        ticket.id = "123-321-456-654"
        sender = helpers.TicketWithQRCodeSender()
        sender.send("test@gmail.com", ticket)
        mock_make.assert_called_with("example.com/api/tickets/check/123-321-456-654/")

    @pytest.mark.django_db
    @patch("applications.tickets.helpers.qrcode.make", return_value=load_mock_image())
    @patch("applications.tickets.helpers.EmailMessage", return_value=email_mock)
    def test_send_sends_EmailMessage_with_correct_data(
        self, email_message: MagicMock, mock_make: MagicMock
    ):
        helpers.time.time = lambda: 123
        ticket: Ticket = mixer.blend("tickets.Ticket")
        ticket.template._file = load_mock_pdf()  # type:ignore
        sender = helpers.TicketWithQRCodeSender()
        sender.send("test@gmail.com", ticket)
        email_message.assert_called_once_with(
            "Hello, Events here",
            "You are getting your own ticket below",
            "events@gmail.com",
            ["test@gmail.com"],
        )
        email_attach_file = cast(MagicMock, self.email_mock.attach_file)
        assert email_attach_file.call_count == 2
        email_attach_file.assert_any_call("media/tmp/123000.png")
        email_attach_file.assert_any_call("media/tmp/123000.pdf")
