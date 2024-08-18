from django.db import models
from core.models import Event
from django.core.validators import FileExtensionValidator
import uuid


"""
If event is private is necessary to get a ticket before arrive to event
Each ticket is generated based on template file with unique key as id of that ticket.
The quantity of tickets depends on promoter of event.
"""


class TicketTemplate(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    _file = models.FileField(
        upload_to="media/tickets/", validators=[FileExtensionValidator(["pdf"])]
    )

    def __str__(self):
        return self.event.title + " Ticket Template"


class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    template = models.ForeignKey(TicketTemplate, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return "Ticket " + str(self.id)
