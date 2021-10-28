from rest_framework import serializers

class TicketSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    