from rest_framework import serializers
from . import validators
from .models import Category, Event, FollowedHashTag, EventHistory
from tickets.helpers import TicketGenerator
from tickets.serializers import TicketTemplateSerializer
from drf_extra_fields.geo_fields import PointField





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
        fields = ('id', 'title', 'location' ,'event_datetime', 'category', 'is_free',)





class EventDetailSerializer(serializers.ModelSerializer):
    ticket = TicketTemplateSerializer(write_only=True, required=False)
    histories = EventHistorySerializer(many=True, read_only=True)
    location = PointField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'promoter', 'took_place',)
        validators = [validators.CheckIfTicketProvidedIfPrivate()]
        extra_kwargs = {
            'category': { 'required': True },
            'location': { 'required': True }
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
        return super(EventDetailSerializer, self).update(instance, validated_data)
        