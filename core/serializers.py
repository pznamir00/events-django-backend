from rest_framework import serializers
from . import validators
from .models import Category, Event, FollowedHashTag, EventHistory
from tickets.helpers import TicketGenerator
from tickets.serializers import TicketTemplateSerializer





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
        read_only_fields = ('slug',)
        
        
        
        
        
class EventHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventHistory
        exclude = ('id',)
        extra_kwargs = {
            'event': { 
                'write_only': True 
            }
        }
        
        
        
        
        
class FollowedHashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowedHashTag
        fields = ('value',)
        
        
        


class EventSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'latitude', 'longitude', 'event_datetime', 'category', 'is_free',)





class EventDetailSerializer(serializers.ModelSerializer):
    ticket = TicketTemplateSerializer(write_only=True, required=False)
    histories = EventHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'promoter', 'took_place',)
        validators = (
            validators.CheckIfTicketProvidedIfPrivate(),
            validators.CheckGeolocation(),
        )
        extra_kwargs = {
            'latitude': { 'required': True },
            'longitude': { 'required': True },
            'category': { 'required': True },
        }
        
    def validate_ticket(self, value):
        if 'quantity' not in value or 'template' not in value:
            raise serializers.ValidationError("Please valid 'ticket' field")
            
    def create(self, validated_data):
        ticket = validated_data.pop('ticket', None)
        event = Event.objects.create(**validated_data)
        TicketGenerator.generate_if_provided(validated_data, ticket, event)
        return event
    
    def update(self, instance, validated_data):
        ticket = validated_data.pop('ticket', None)
        TicketGenerator.generate_if_provided(validated_data, ticket, instance)
        instance.save(**validated_data)
        return instance
        