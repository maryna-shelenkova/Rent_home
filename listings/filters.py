import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    rooms_min = django_filters.NumberFilter(field_name="rooms", lookup_expr='gte')
    rooms_max = django_filters.NumberFilter(field_name="rooms", lookup_expr='lte')
    location = django_filters.CharFilter(field_name="location", lookup_expr='icontains')
    type = django_filters.CharFilter(field_name="type", lookup_expr='iexact')

    class Meta:
        model = Listing
        fields = ['price_min', 'price_max', 'rooms_min', 'rooms_max', 'location', 'type']



