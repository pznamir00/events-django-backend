from rest_framework import serializers
import base64


class CheckIfTicketProvidedIfPrivate:
    def __call__(self, value):
        if value.get('is_free') == False:
            if 'ticket' not in value:
                raise serializers.ValidationError("If you are passing is_free field, you must pass ticket field too")
            