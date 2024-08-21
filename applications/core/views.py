from typing import Union
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from django.template.defaultfilters import slugify
from django_filters import rest_framework as filters
from .serializers import (
    CategorySerializer,
    EventDetailSerializer,
    EventSimpleSerializer,
    FollowedHashTagSerializer,
)
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
    viewsets.GenericViewSet,
):
    serializer_class = FollowedHashTagSerializer

    def get_queryset(self):  # type: ignore
        return FollowedHashTag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # change string to hashtag
        value = serializer.validated_data.pop("value")
        value = slugify(value).replace("-", "")
        # save data
        return serializer.save(user=self.request.user, value=value)


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
    filter_class = EventFilterSet
    ordering_fields = (
        "distance",
        "event_datetime_expired",
        "-create_at",
    )

    def get_serializer_class(self):  # type: ignore
        """
        For list method user can get simplify version of objects.
        """
        return EventSimpleSerializer if self.action == "list" else EventDetailSerializer

    def perform_create(self, serializer):
        return serializer.save(promoter=self.request.user)

    def perform_update(
        self, serializer: Union[EventSimpleSerializer, EventDetailSerializer]
    ):
        """
        In this point application creates history logs.
        Each of them is generated automatically based on
        updated properties
        """
        event = serializer.instance
        assert isinstance(serializer.validated_data, dict)
        if "event_datetime" in serializer.validated_data:
            assert isinstance(serializer.instance, Event)
            # Changed event datetime
            text = (
                str(serializer.instance.event_datetime)
                + " ===> "
                + str(serializer.validated_data["event_datetime"])
            )
            EventHistory.objects.create(event=event, label="1", text=text)
        if serializer.validated_data.get("took_place"):
            # The event took place
            EventHistory.objects.create(event=event, label="4")
        if serializer.validated_data.get("canceled"):
            # Canceled an event
            EventHistory.objects.create(event=event, label="2")
        else:
            # Note update
            EventHistory.objects.create(event=event, label="3")
        return serializer.save()


class EventOwnListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EventSimpleSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):  # type: ignore
        return Event.objects.filter(promoter=self.request.user)
