from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserPlatformChoice, Item, ItemOffer
from .serializers import UserPlatformChoiceSerializer, ItemSerializer, ItemOfferSerializer


class UserPlatformChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = UserPlatformChoiceSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, request):
        return UserPlatformChoice.objects.filter(user=request.user)
    
    def perform_create(self, instance):
        return instance.save(user = self.request.user)
    
    
class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, request):
        return Item.objects.filter(user=request.user)