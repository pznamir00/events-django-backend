from rest_framework import serializers, viewsets, mixins, generics
from .serializers import CategorySerializer, EventDetailSerializer, EventSimpleSerializer, FollowedHashTagSerializer
from .models import Category, FollowedHashTag, Event
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
import uuid





class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    
    
    
    
    
class FollowedHashTagView(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    mixins.DestroyModelMixin, 
    viewsets.GenericViewSet
):
    serializer_class = FollowedHashTagSerializer
    
    def get_queryset(self, request):
        return FollowedHashTag.objects.filter(user=request.user)
    
    def perform_create(self, instance):
        return instance.save(user=self.request.user)
    
    
    

    
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permissions_classes = (IsOwnerOrReadOnly,)
    
    def get_serializer_class(self):
        """
        For list method user can get simplify version of objects.
        """
        return EventSimpleSerializer if self.action == 'list' else EventDetailSerializer
    
    def perform_create(self, instance):
        return instance.save(
            user=self.request.user,
            secret_key=uuid.uuid64()
        )
    
    
    
    
    
class EventOwnListView(generics.ListAPIView):
    serializer_class = EventDetailSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, request):
        return Event.objects.filter(user=request.user)