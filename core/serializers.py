from rest_framework import serializers
from .models import Category, Event, EventImage, FollowedHashTag, EventHistory
from django_base64field.fields import Base64Field





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
        read_only = ('slug',)
        
        
        
        
        
class EventHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventHistory
        fields = ('label', 'text',)
        
        
        
        
        
class EventImageSerializer(serializers.ModelSerializer):
    file = Base64Field(write_only=True)
    
    class Meta:
        model = EventImage
        fields = ('event', 'file',)
        
        
        
        
        
class FollowedHashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowedHashTag
        fields = ('value',)
        
        
        


class EventSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'geolocation', 'event_datetime', 'category', 'is_free',)





class EventDetailSerializer(serializers.ModelSerializer):
    images = Base64Field(many=True)
    histories = EventHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'