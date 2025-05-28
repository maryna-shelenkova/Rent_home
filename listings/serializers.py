from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Listing — преобразует объекты в JSON и обратно
    class Meta:
        model = Listing
        fields = '__all__'  # Можно указать конкретные поля, если нужно
        read_only_fields = ('owner',)  # Владельца назначим автоматически, менять нельзя

