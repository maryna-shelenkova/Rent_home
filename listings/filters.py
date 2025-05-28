import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')  # Цена от
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')  # Цена до
    min_rooms = django_filters.NumberFilter(field_name='rooms', lookup_expr='gte')  # Кол-во комнат от
    max_rooms = django_filters.NumberFilter(field_name='rooms', lookup_expr='lte')  # Кол-во комнат до
    location = django_filters.CharFilter(lookup_expr='icontains')  # Частичный поиск по местоположению
    property_type = django_filters.CharFilter(lookup_expr='iexact')  # Тип жилья

    class Meta:
        model = Listing
        fields = ['min_price', 'max_price', 'min_rooms', 'max_rooms', 'location', 'property_type']
