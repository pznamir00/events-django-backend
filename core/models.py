from django.db import models
from users.models import User
from autoslug import AutoSlugField
from .choices import HistoryLabel
import uuid




"""
Basic category model
Slug is generating based on the name after creating
"""
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name




"""
Main Event model.
It includes all necessery data for schedule a meeting (place, time etc.)
This objects have own images and history additionally.
If is_private = True, secret key is generated as random key for sharing by link,
If is_free = True, tickets are necessery and are stored in tickets table.
"""
class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    geolocation = models.PointField(geography=True)
    location_hints = models.CharField(max_length=256, blank=True, null=True)
    event_datetime = models.DateTimeField()
    promoter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_free = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    secret_key = models.UUIDField(editable=False, unique=True, blank=True, null=True)
    took_place = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    
    
    
"""
Images for event
"""
class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='media/events/')
    
    def __str__(self):
        return self.file.name
    
    
    
    
"""
Histories for events.
Include all additional informations for client about currenc state of event,
(i.e. event is canceled).
Label field includes the name of that log.
"""
class EventHistory(models.Model):
    label = models.CharField(max_length=1, choices=HistoryLabel)
    text = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
    

"""
Authorized users can incidate hashtags that belong to events 
for getting easy access and find quickty new events.
"""
class FollowedHashTag(models.Model):
    value = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return '#' + self.value
    
    
    
    
"""
If event is private is necessery to get a ticket before arrive to event
Each ticket is generated based on template file with unique key as id of that ticket.
The quantity of tickets depends on promotor of event.
"""
class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    template = models.FileField(upload_to='media/tickets/')
    sold = models.BooleanField(default=False)
    
    def __str__(self):
        return self.id












