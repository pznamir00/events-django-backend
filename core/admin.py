from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Event)
admin.site.register(models.EventHistory)
admin.site.register(models.EventTicket)
