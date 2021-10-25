from rest_framework import serializers
from .models import Category, Event, EventImage, FollowedHashTag, EventHistory, EventTicket
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
    file = Base64Field()
    
    class Meta:
        model = EventImage
        fields = ('event', 'file',)
        extra_kwargs = {
            'file': { 'write_only': True }
        }
        
        
        
        
        
class FollowedHashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowedHashTag
        fields = ('value',)





class EventTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTicket
        fields = ('template',)

        
        


class EventSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'geolocation', 'event_datetime', 'category', 'is_free',)





class EventDetailSerializer(serializers.ModelSerializer):
    ticket = EventTicketSerializer(write_only=True)    
    images = Base64Field()
    histories = EventHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'
        
    def validate_is_private(self):
        if self.is_free:
            if not self.template:
                return serializers.ValidationError("If you are passing is_free field, you must pass template field too")
            
    def create(self, validated_data):
        template = validated_data.pop('template', None)
        event = Event.objects.create(**validated_data)
        if not event.is_free:
            EventTicket.objects.create(
                event=event, 
                template=template
            )
        return event