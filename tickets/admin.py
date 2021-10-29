from django.contrib import admin
from . import models

admin.site.register(models.TicketTemplate)
admin.site.register(models.Ticket)
