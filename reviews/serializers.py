from rest_framework import serializers
from .models import Review, Listing


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'listing')

    def create(self, validated_data):
        user = self.context['request'].user
        listing = validated_data['listing']

        review, created = Review.objects.update_or_create(
            user=user,
            listing=listing,
            defaults={
                'rating': validated_data['rating'],
                'comment': validated_data['comment'],
            }
        )
        return review

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class ListingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 1)
        return None


