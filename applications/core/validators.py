from rest_framework import serializers


class CheckIfTicketProvidedIfPrivate:
    def __call__(self, value: dict):
        if not value.get("is_free"):
            if "ticket" not in value:
                raise serializers.ValidationError(
                    "If you are passing is_free field, you must pass ticket field too"
                )
