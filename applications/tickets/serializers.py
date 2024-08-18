from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import Ticket, TicketTemplate


class TicketPurchaseSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ("template",)


class TicketTemplateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(
        required=True, validators=[MinValueValidator(0)]
    )

    class Meta:
        model = TicketTemplate
        fields = (
            "template",
            "quantity",
        )
