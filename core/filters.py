from rest_framework.serializers import ValidationError
from django.db.models import Q
from .models import Event
import django_filters as filters
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

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
        try:
            lat = self.request.query_params.get('latitude', None)
            lon = self.request.query_params.get('longitude', None)
            point = Point(lat, lon)
        except:
            raise ValidationError("Excepted 'lat' and 'lon' parameters (both decimal) when you pass 'range' field")
        return queryset.filter(
            location__dwithin=(
                point, 
                D(km=value)
            )
        )

    def filter_by_keywords(self, queryset, name, value):
        """
        Filter by 3 fields (title, description and location_hints)
        """
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(description__icontains=value) | 
            Q(location_hints__icontains=value)
        )
