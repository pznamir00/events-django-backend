from typing import Union
from rest_framework import viewsets, mixins
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from applications.core.services import EventService, SlugService
from .serializers import (
    EventDetailSerializer,
    EventSimpleSerializer,
    FollowedHashTagSerializer,
)
from .models import FollowedHashTag, Event
from .permissions import IsOwnerOrReadOnly, CreateAuthenticatedOnly
from .filters import EventFilterSet, EventOrderingFilter


class FollowedHashTagView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FollowedHashTagSerializer
    permission_classes = (IsAuthenticated,)
    slug_service = SlugService()

    def get_queryset(self):
        return FollowedHashTag.objects.filter(user=self.request.user)

    def perform_create(self, serializer: Serializer):
        data: dict = serializer.validated_data
        slug = self.slug_service.create_slug(data.pop("value"))
        return serializer.save(user=self.request.user, value=slug)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_private=False, canceled=False, took_place=False)
    permission_classes = (
        IsOwnerOrReadOnly,
        CreateAuthenticatedOnly,
    )
    filter_backends = (
        filters.DjangoFilterBackend,
        EventOrderingFilter,
    )
    filterset_class = EventFilterSet
    ordering_fields = (
        "distance",
        "event_datetime_expired",
        "-create_at",
    )
    event_service = EventService()

    def get_serializer_class(self):
        """
        For list method user can get simplify version of objects.
        """
        return EventSimpleSerializer if self.action == "list" else EventDetailSerializer

    def perform_create(self, serializer: Serializer):
        return serializer.save(promoter=self.request.user)

    def perform_update(
        self, serializer: Union[EventSimpleSerializer, EventDetailSerializer]
    ):
        """
        In this point application creates history logs.
        Each of them is generated automatically based on
        updated properties
        """
        event: Event = serializer.instance
        changes: dict = serializer.validated_data
        self.event_service.register_event_history_base_on_changes(event, changes)
        return serializer.save()


class EventOwnListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EventSimpleSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Event.objects.filter(promoter=self.request.user)
