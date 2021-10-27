from rest_framework import serializers


class CheckIfTicketProvidedIfPrivate:
    def __call__(self, value):
        if 'is_free' in value and not value['is_free']:
            if 'template' not in value:
                raise serializers.ValidationError("If you are passing is_free field, you must pass template field too")
            

class CheckGeolocation:
    def __call__(self, value):
        if 'latitude' in value and 'longitude' in value:
            if not (0 <= value['latitude'] <= 180.00 and 0 <= value['longitude'] <= 180.00):
                raise serializers.ValidationError("You passed wrong coordinates")