from rest_framework import serializers
from .models import TicketTemplate
from django.core.validators import MinValueValidator





class TicketSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)





class TicketTemplateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=True, validators=[MinValueValidator(0)])
    
    class Meta:
        model = TicketTemplate
        fields = ('template', 'quantity',)