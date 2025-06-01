from django.db.models import Avg, Count
from rest_framework import serializers
from listings.models import Listing

class ListingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = '__all__'

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else None

    def get_reviews_count(self, obj):
        return obj.reviews.count()


