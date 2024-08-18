from django.db import models


class HistoryLabel(models.TextChoices):
    MOVED = "1", "Moved"
    CANCELED = "2", "Canceled"
    DETAILS_CHANGED = "3", "Details Changed"
    TOOK_PLACE = "4", "Took place"
