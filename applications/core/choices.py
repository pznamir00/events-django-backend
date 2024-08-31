from django.db import models


class HistoryLabel(models.TextChoices):
    MOVED = "1", "Moved"
    CANCELED = "2", "Canceled"
    DETAILS_CHANGED = "3", "Details Changed"
    TOOK_PLACE = "4", "Took place"


class Category(models.TextChoices):
    MUSIC_FESTIVAL = "1", "Music Festival"
    ART_EXHIBITION = "2", "Art Exhibition"
    CONCERT = "3", "Concert"
    THEATRE_PERFORMANCE = "4", "Theatre performance"
    MOVIE_FESTIVAL = "5", "Movie Festival"
