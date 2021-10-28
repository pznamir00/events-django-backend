from django.db import models
from core.models import EventTemplate
import uuid


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    template = models.ForeignKey(EventTemplate, on_delete=models.CASCADE)
    sold = models.BooleanField(default=False)
    
    def __str__(self):
        return "Ticket " + str(self.id)