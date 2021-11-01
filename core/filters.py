from rest_framework.serializers import ValidationError
from django.db.models import Q
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from rest_framework.filters import OrderingFilter
from django.db.models import Case, When, Value
from django.contrib.gis.db.models.functions import Distance
from datetime import datetime
from .models import Event
import django_filters as filters





class EventFilterSet(filters.FilterSet):
    range = filters.NumberFilter(method='filter_by_range')
    keywords = filters.CharFilter('keywords', method='filter_by_keywords')
    created_at = filters.DateRangeFilter()
    updated_at = filters.DateRangeFilter()
    event_datetime = filters.DateRangeFilter()
    category = filters.NumberFilter('category')
    promoter = filters.NumberFilter('promoter')
    is_free = filters.BooleanFilter('is_free')

    class Meta:
        model = Event
        fields = [
            'keywords',
            'created_at', 
            'updated_at', 
            'event_datetime', 
            'category', 
            'promoter', 
            'is_free'
        ]
        
    def filter_by_range(self, queryset, name, value):     
        """
        This filters queryset by range.
        Get only this events that location is inside a range in 
        radius (field 'range') from user's location
        (fields 'latitude' and 'longitude' are required)
        """       
        try:
            lat = self.request.query_params['latitude']
            lon = self.request.query_params['longitude']
            point = Point(float(lat), float(lon))
        except:
            raise ValidationError("Excepted 'latitude' and 'longitude' parameters (both decimal) when you pass 'range' field")
        return queryset.filter(location__dwithin=(point, D(km=value)))

    def filter_by_keywords(self, queryset, name, value):
        """
        Filter by 3 fields (title, description and location_hints)
        """
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(description__icontains=value) | 
            Q(location_hints__icontains=value)
        )





class EventOrderingFilter(OrderingFilter):
    """
    Default ordering way for events list.
    That orders by time expiriation and if user
    provided coordinates, by distance either.
    """
    def filter_queryset(self, request, queryset, view):
        """
        Order by expiriation time. Expired events go to the end of a list.
        """
        queryset.annotate(
            event_datetime_expired=Case(
                When(event_datetime__lte=datetime.now(), then=Value('0')),
                default=Value('1')
            )
        )
        
        try:  
            """
            Order by distance if lat and lon are provided.
            """
            lat = self.request.query_params.get('latitude')
            lon = self.request.query_params.get('longitude')
            queryset.annotate(distance=Distance("location", Point(float(lat), float(lon))))
        except:
            queryset.annotate(distance=Value(0))
        
        return queryset
