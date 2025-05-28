from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  # сериализуем все поля
        read_only_fields = ('user', 'created_at')  # пользователь и дата создаются автоматически
