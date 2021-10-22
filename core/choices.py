from django.db import models

class HistoryLabel(models.TextChoices):
    MOVED = '1', 'Moved'
    DETAILS_CHANGED = '2', 'Details Changed'
    CANCELED = '3', 'Canceled'