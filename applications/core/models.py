import uuid
from autoslug import AutoSlugField
from django.contrib.gis.db.models import PointField
from django.db import models
from applications.users.models import User
from .choices import HistoryLabel
from .helpers import EventFileNameGenerator


class Category(models.Model):
    """
    Basic category model
    Slug is generating based on the name after creating
    """

    name = models.CharField(max_length=64, unique=True)
    slug = AutoSlugField(populate_from="name")

    def __str__(self):
        return f"{self.name}"


class Event(models.Model):
    """
    Main Event model.
    It includes all necessary data for schedule a meeting (place, time etc.)
    This objects have own images and history additionally.
    If is_private = True, secret key is generated as random key for sharing by link,
    If is_free = True, tickets are necessary and are stored in tickets table.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = PointField(geography=True, null=True)
    location_hints = models.CharField(max_length=256, blank=True, null=True)
    event_datetime = models.DateTimeField()
    promoter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_free = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    took_place = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=EventFileNameGenerator.generate, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title}"


class EventHistory(models.Model):
    """
    Histories for events.
    Include all additional information for client about current state of event,
    (i.e. event is canceled).
    Label field includes the name of that log.
    """

    label = models.CharField(max_length=1, choices=HistoryLabel.choices)
    text = models.CharField(max_length=256, blank=True, null=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="histories", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label}"


class FollowedHashTag(models.Model):
    """
    Authorized users can point hashtags that belong to events
    for getting easy access and find quickly new events.
    """

    value = models.CharField(max_length=128)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed_hashtags"
    )

    def __str__(self):
        return f"#{self.value}"
