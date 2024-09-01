from datetime import datetime
from typing import Any
from django.db.models import Q
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.db.models import Case, When, Value, QuerySet
from django.contrib.gis.db.models.functions import Distance
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request
from rest_framework.views import View  # type:ignore
from rest_framework.serializers import ValidationError
import django_filters as filters
from applications.core.services import FilterService
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
    filter_service = FilterService()

    class Meta:
        model = Event
        fields = (
            "keywords",
            "created_at",
            "updated_at",
            "event_datetime",
            "category",
            "promoter",
            "is_free",
        )

    def filter_by_range(self, queryset: QuerySet, _: Any, value: float):
        """
        This filters queryset by range.
        Get only this events that location is inside a range in
        radius (field 'range') from user's location
        (fields 'latitude' and 'longitude' are required)
        """
        req: Request = self.request
        lat_lon = self.filter_service.get_lat_lon_from_query_params(req)
        if not lat_lon:
            raise ValidationError(
                {
                    "range": [
                        "range parameter requires both latitude and longitude params"
                    ]
                }
            )

        lat, lon = lat_lon
        return queryset.filter(location__dwithin=(Point(lat, lon), D(km=value)))

    def filter_by_keywords(self, queryset: QuerySet, _: Any, value: str):
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

    filter_service = FilterService()

    def filter_queryset(self, request: Request, queryset: QuerySet, view: View):
        # set datetime_expired annotation
        queryset = queryset.annotate(
            event_datetime_expired=Case(
                When(event_datetime__lte=datetime.now(), then=Value("0")),
                default=Value("1"),
            )
        )

        # set distance annotation
        lat_lon = self.filter_service.get_lat_lon_from_query_params(request)
        queryset = queryset.annotate(
            distance=(
                Distance("location", Point(lat_lon[0], lat_lon[1], srid=4326))
                if lat_lon
                else Value(0)
            )
        )

        return super().filter_queryset(request, queryset, view)
