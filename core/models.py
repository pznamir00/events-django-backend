from django.db import models
from users.models import User
from autoslug import AutoSlugField
from .choices import HistoryLabel
from .helpers import EventFileNameGenerator
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
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=3, default=0.00)
    latitude = models.DecimalField(max_digits=8, decimal_places=3, default=0.00)
    location_hints = models.CharField(max_length=256, blank=True, null=True)
    event_datetime = models.DateTimeField() 
    promoter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_free = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    took_place = models.BooleanField(default=False)
    image = models.ImageField(upload_to=EventFileNameGenerator.generate, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
    
    
    
"""
Histories for events.
Include all additional informations for client about currenc state of event,
(i.e. event is canceled).
Label field includes the name of that log.
"""
class EventHistory(models.Model):
    label = models.CharField(max_length=1, choices=HistoryLabel.choices)
    text = models.CharField(max_length=256, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='histories', null=True)
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
    











