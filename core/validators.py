from rest_framework import serializers
import base64


class CheckIfTicketProvidedIfPrivate:
    def __call__(self, value):
        if 'is_free' in value and not value['is_free']:
            if 'ticket_template' not in value:
                raise serializers.ValidationError("If you are passing is_free field, you must pass ticket_template field too")
            

class CheckGeolocation:
    def __call__(self, value):
        if 'latitude' in value and 'longitude' in value:
            if not (0 <= value['latitude'] <= 180.00 and 0 <= value['longitude'] <= 180.00):
                raise serializers.ValidationError("You passed wrong coordinates")
            

class CheckIsPureTextEncodedPdfFile:
    def __call__(self, value):
        try:
            text = value['template']
            res = base64.b64decode(text)
            print(res)
        except:
            raise serializers.ValidationError("Please pass valid pdf file")