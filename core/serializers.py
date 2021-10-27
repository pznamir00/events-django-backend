from rest_framework import serializers
from . import validators
from .models import Category, Event, FollowedHashTag, EventHistory, EventTicket
from drf_extra_fields.fields import Base64ImageField





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
        read_only_fields = ('slug',)
        
        
        
        
        
class EventHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventHistory
        fields = ('label', 'event',)
        
        
        
        
        
class FollowedHashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowedHashTag
        fields = ('value',)





class EventTicketSerializer(serializers.ModelSerializer):
    template = Base64ImageField()
    quantity = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = EventTicket
        fields = ('template', 'quantity',)

        
        


class EventSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'latitude', 'longitude', 'event_datetime', 'category', 'is_free',)





class EventDetailSerializer(serializers.ModelSerializer):
    ticket = EventTicketSerializer(write_only=True, required=False)
    histories = EventHistorySerializer(many=True, read_only=True)
    image_input = Base64ImageField(write_only=True, required=False)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'promoter', 'image', 'took_place',)
        validators = (
            validators.CheckIfTicketProvidedIfPrivate(),
            validators.CheckGeolocation()
        )
        extra_kwargs = {
            'latitude': { 'required': True },
            'longitude': { 'required': True },
            'category': { 'required': True },
        }
            
    def create(self, validated_data):
        ticket = validated_data.pop('ticket', None)
        image = validated_data.pop('image_input', None)
        event = Event.objects.create(**validated_data, image=image)
        if not event.is_free:
            EventTicket.objects.create(
                event=event, 
                template=ticket,
            )
        return event