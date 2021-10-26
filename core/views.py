from rest_framework import viewsets, mixins
from .serializers import CategorySerializer, EventDetailSerializer, EventSimpleSerializer, FollowedHashTagSerializer
from django.db.models import Case, When, Value
from .models import Category, FollowedHashTag, Event
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, CreateAuthenticatedOnly
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.template.defaultfilters import slugify
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
    
    def get_queryset(self):
        return FollowedHashTag.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        #change string to hashtag
        value = serializer.validated_data.pop('value')
        value = slugify(value).replace('-', '')
        #save data
        return serializer.save(
            user=self.request.user,
            value=value
        )
    
    
    

    
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventDetailSerializer
    permission_classes = (CreateAuthenticatedOnly, IsOwnerOrReadOnly,)
    
    def get_queryset(self):
        return Event.objects.filter(
            active=True,
            is_private=False
        ).annotate(
            event_datetime_expired=Case(
                When(event_datetime__lte=datetime.now(), then=Value('0')),
                default=Value('1')
            )
        ).order_by(
            'event_datetime_expired',
            '-created_at'
        )
    
    def get_serializer_class(self):
        """
        For list method user can get simplify version of objects.
        """
        return EventSimpleSerializer if self.action == 'list' else EventDetailSerializer
    
    def perform_create(self, serializer):
        data = { 'promoter': self.request.user }
        if 'is_private' in serializer.validated_data and serializer.validated_data['is_private']:
            data['secret_key'] = uuid.uuid64
        return serializer.save(**data)
    
    
    
    
    
class EventOwnListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EventDetailSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Event.objects.filter(promoter=self.request.user)