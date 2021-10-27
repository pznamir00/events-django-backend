from rest_framework import serializers
from . import validators
from .models import Category, Event, EventTemplate, FollowedHashTag, EventHistory, EventTicket
from drf_extra_fields.fields import Base64ImageField
import base64 




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





class EventTemplateSerializer(serializers.ModelSerializer):
    template = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)
    
    class Meta:
        model = EventTemplate
        fields = ('template', 'quantity',)
        
        
        


class EventSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'latitude', 'longitude', 'event_datetime', 'category', 'is_free',)





class EventDetailSerializer(serializers.ModelSerializer):
    ticket_template = EventTemplateSerializer(write_only=True, required=False)
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
        image = validated_data.pop('image_input', None)
        ticket_template = validated_data.pop('ticket_template', None)
        event = Event.objects.create(**validated_data, image=image)
        if not event.is_free:
            # save a template
            template_file = base64.b64decode(ticket_template['template'])
            template = EventTemplate.objects.create(event=event, template=template_file)
            for i in range(ticket_template['quantity']):
                # creating single tickets
                EventTicket.objects.create(template=template)
        return event