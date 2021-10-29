import django_filters as filters
from django.db.models import Q

class EventFilterSet(filters.FilterSet):
    keywords = filters.CharFilter(label='keywords', method='keywords_lookup_field')
    created_at = filters.DateTimeFromToRangeFilter()
    updated_at = filters.DateTimeFromToRangeFilter()
    event_datetime = filters.DateTimeFromToRangeFilter()
    category = filters.NumberFilter('category')
    promoter = filters.NumberFilter('promoter')
    is_free = filters.BooleanFilter('is_free')

    class Meta:
        model = Product
        fields = [
            'keywords'
            'created_at', 
            'updated_at', 
            'event_datetime', 
            'category', 
            'promoter', 
            'is_free'
        ]

    def keywords_lookup_fields(self, queryset, name, value):
        """
        Filter by 3 fields (title, description and location_hints)
        """
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(description__icontains=value) | 
            Q(location_hints__icontains=value)
        )
