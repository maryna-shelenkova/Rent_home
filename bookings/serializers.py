from rest_framework import serializers
from .models import Booking
from datetime import date


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at')

def validate(self, data):
    if data['start_date'] >= data['end_date']:
        raise serializers.ValidationError("End date must be after start date.")
    if data['start_date'] < date.today():
        raise serializers.ValidationError("Start date cannot be in the past.")
    return data
