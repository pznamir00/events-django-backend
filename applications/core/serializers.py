from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from applications.tickets.helpers import TicketGenerator
from applications.tickets.serializers import TicketTemplateSerializer
from . import validators
from .models import Category, Event, FollowedHashTag, EventHistory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )
        read_only_fields = ("slug",)


class EventHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventHistory
        exclude = ("id",)
        extra_kwargs = {"event": {"write_only": True}}


class FollowedHashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowedHashTag
        fields = ("value",)


class EventSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "location",
            "event_datetime",
            "category",
            "is_free",
        )


class EventDetailSerializer(serializers.ModelSerializer):
    ticket = TicketTemplateSerializer(write_only=True, required=False)
    histories = EventHistorySerializer(many=True, read_only=True)
    location = PointField()

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
            "promoter",
            "took_place",
        )
        validators = [validators.CheckIfTicketProvidedIfPrivate()]
        extra_kwargs = {"category": {"required": True}, "location": {"required": True}}

    def validate_ticket(self, value):
        if "quantity" not in value or "template" not in value:
            raise serializers.ValidationError("Please valid 'ticket' field")

    def create(self, validated_data):
        ticket = validated_data.pop("ticket", None)
        event = Event.objects.create(**validated_data)
        self.__generate_tickets_if_needed(validated_data, ticket, event)
        return event

    def update(self, instance, validated_data):
        ticket = validated_data.pop("ticket", None)
        self.__generate_tickets_if_needed(validated_data, ticket, instance)
        return super().update(instance, validated_data)

    def __generate_tickets_if_needed(self, data: dict, ticket: dict, event: Event):
        ticket_generator = TicketGenerator(data)
        if ticket_generator.should_generate_tickets():
            ticket_generator.generate_tickets(ticket, event)
