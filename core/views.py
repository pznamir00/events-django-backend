from rest_framework import viewsets, mixins, generics
from .serializers import CategorySerializer, EventDetailSerializer, EventSimpleSerializer, FollowedHashTagSerializer
from django.db.models import Case, When, Value, BooleanField
from .models import Category, FollowedHashTag, Event
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
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
    serializer_class = EventDetailSerializer
    permissions_classes = (IsOwnerOrReadOnly,)
    
    def get_queryset(self, request):
        return Event.objects.filter(
            active=True,
            is_private=False
        ).annotate(
            event_datetime_expired=Case(
                When(event_datetime__lte=datetime.now(), then=Value('0')),
                default=Value('1')
            )
        ).order_by(
            'event_datetime_expired'
            '-created_at'
        )
    
    def get_serializer_class(self):
        """
        For list method user can get simplify version of objects.
        """
        return EventSimpleSerializer if self.action == 'list' else EventDetailSerializer
    
    def perform_create(self, instance):
        secret_key = uuid.uuid64 if instance.is_private else None
        return instance.save(
            user=self.request.user,
            secret_key=secret_key
        )
    
    
    
    
    
class EventOwnListView(generics.ListAPIView):
    serializer_class = EventDetailSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, request):
        return Event.objects.filter(user=request.user)