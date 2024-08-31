from rest_framework import serializers


class CheckIfTicketProvidedIfPrivate:
    def __call__(self, value: dict):
        if "is_free" in value and not value["is_free"] and "ticket" not in value:
            raise serializers.ValidationError(
                "If you are passing is_free field, you must pass ticket field too"
            )
