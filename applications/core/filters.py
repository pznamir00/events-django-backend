from datetime import datetime
from django.db.models import Q
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.db.models import Case, When, Value, QuerySet
from django.contrib.gis.db.models.functions import Distance
from rest_framework.serializers import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request
import django_filters as filters
from .models import Event


class EventFilterSet(filters.FilterSet):
    range = filters.NumberFilter(method="filter_by_range")
    keywords = filters.CharFilter("keywords", method="filter_by_keywords")
    created_at = filters.DateRangeFilter()
    updated_at = filters.DateRangeFilter()
    event_datetime = filters.DateRangeFilter()
    category = filters.NumberFilter("category")
    promoter = filters.NumberFilter("promoter")
    is_free = filters.BooleanFilter("is_free")

    class Meta:
        model = Event
        fields = [
            "keywords",
            "created_at",
            "updated_at",
            "event_datetime",
            "category",
            "promoter",
            "is_free",
        ]

    def filter_by_range(self, queryset, _, value):
        """
        This filters queryset by range.
        Get only this events that location is inside a range in
        radius (field 'range') from user's location
        (fields 'latitude' and 'longitude' are required)
        """
        try:
            assert isinstance(self.request, Request)
            lat = self.request.query_params["latitude"]
            lon = self.request.query_params["longitude"]
            point = Point(float(lat), float(lon))
        except Exception as exc:
            raise ValidationError(
                """
                Excepted 'latitude' and 'longitude' parameters
                (both decimal) when you pass 'range' field
                """
            ) from exc
        return queryset.filter(location__dwithin=(point, D(km=value)))

    def filter_by_keywords(self, queryset: QuerySet, _, value):
        """
        Filter by 3 fields (title, description and location_hints)
        """
        return queryset.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(location_hints__icontains=value)
        )


class EventOrderingFilter(OrderingFilter):
    """
    Default ordering way for events list.
    That orders by time expiration and if user
    provided coordinates, by distance either.
    """

    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        """
        Order by expiration time. Expired events go to the end of a list.
        """
        queryset = queryset.annotate(
            event_datetime_expired=Case(
                When(event_datetime__lte=datetime.now(), then=Value("0")),
                default=Value("1"),
            )
        )

        try:
            # Order by distance if lat and lon are provided.
            lat = request.query_params.get("latitude", "")
            lon = request.query_params.get("longitude", "")
            assert lat.isnumeric() and lon.isnumeric()
            queryset = queryset.annotate(
                distance=Distance("location", Point(float(lat), float(lon), srid=4326))
            )
        except AssertionError:
            queryset = queryset.annotate(distance=Value(0))

        return super().filter_queryset(request, queryset, view)
