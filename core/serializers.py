from rest_framework import serializers
from .models import UserPlatformChoice, Item, ItemOffer
from .validators import PlatformAuthDataValidator


class UserPlatformChoiceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserPlatformChoice
        fields = ('platform', 'data',)
        validators = (PlatformAuthDataValidator,)
        
        
class ItemOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOffer
        fields = ('platform', 'url',)
        
        
class ItemSerializer(serializers.ModelSerializer):
    offers = ItemOfferSerializer(many=True, read_only=True)
    
    class Meta:
        model = Item
        fields = '__all__'