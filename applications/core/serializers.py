from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from applications.core.services import TicketGeneratorService
from applications.tickets.serializers import TicketTemplateSerializer
from . import validators
from .models import Event, FollowedHashTag, EventHistory


class _EventHistorySerializer(serializers.ModelSerializer):
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
    histories = _EventHistorySerializer(many=True, read_only=True)
    location = PointField()
    ticket_generator_service = TicketGeneratorService()

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
        extra_kwargs = {
            "category": {"required": True},
            "location": {"required": True},
        }

    def validate_ticket(self, value: dict):
        if "quantity" not in value or "file" not in value:
            raise serializers.ValidationError(
                "'ticket' field must contain both quantity and file"
            )

    def create(self, validated_data: dict):
        ticket = validated_data.pop("ticket", None)
        event = Event.objects.create(**validated_data)
        self.ticket_generator_service.generate_if_needed(validated_data, ticket, event)
        return event

    def update(self, instance: Event, validated_data: dict):
        ticket = validated_data.pop("ticket", None)
        self.ticket_generator_service.generate_if_needed(
            validated_data, ticket, instance
        )
        return super().update(instance, validated_data)
