from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from rest_framework import viewsets, permissions
from .permissions import IsOwnerOrReadOnly
from bookings.models import Booking
from rest_framework.exceptions import PermissionDenied

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        listing_id = self.kwargs.get('listing_id')
        return Review.objects.filter(listing_id=listing_id)

    def perform_create(self, serializer):
        listing_id = self.kwargs.get('listing_id')
        user = self.request.user


        has_booking = Booking.objects.filter(
            user=user,
            listing_id=listing_id,
            status='confirmed'
        ).exists()

        if not has_booking:
            raise PermissionDenied("You can only leave a review if you've booked this listing.")

        serializer.save(user=user, listing_id=listing_id)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
