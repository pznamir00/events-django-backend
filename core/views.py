from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.template.defaultfilters import slugify
from django_filters import rest_framework as filters
from .serializers import CategorySerializer, EventDetailSerializer, EventSimpleSerializer, FollowedHashTagSerializer
from .models import Category, EventHistory, FollowedHashTag, Event
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, CreateAuthenticatedOnly
from .filters import EventFilterSet, EventOrderingFilter





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
    queryset = Event.objects.filter(is_active=True, is_private=False)
    serializer_class = EventDetailSerializer
    permission_classes = (IsOwnerOrReadOnly, CreateAuthenticatedOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EventFilterSet
    filter_backends = (EventOrderingFilter,)
    ordering_fields = ('distance', 'event_datetime_expired', '-create_at',)
    
    def get_serializer_class(self):
        """
        For list method user can get simplify version of objects.
        """
        return EventSimpleSerializer if self.action == 'list' else EventDetailSerializer
    
    def get_object(self):
        return get_object_or_404(Event, id=self.kwargs['pk'])
    
    def perform_create(self, serializer):
        return serializer.save(promoter=self.request.user)
    
    def perform_update(self, serializer):
        """
        In this point application creates history logs.
        Each of them is generated automatically based on 
        updated properties
        """
        event = serializer.instance
        if 'event_datetime' in serializer.validated_data:
            #Changed event datetime
            text = str(serializer.instance.event_datetime) + " ===> " + str(serializer.validated_data['event_datetime'])
            EventHistory.objects.create(event=event, label='1', text=text)
        if serializer.validated_data.get('took_place'):
            #The event took place
            EventHistory.objects.create(event=event, label='4')
        if serializer.validated_data.get('is_active') == False:
            #Canceled an event
            EventHistory.objects.create(event=event, label='2')
        else:
            #Note update
            EventHistory.objects.create(event=event, label='3')
        return serializer.save()
    
    
    
    
    
class EventOwnListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EventSimpleSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Event.objects.filter(promoter=self.request.user)