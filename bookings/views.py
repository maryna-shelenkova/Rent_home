from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from datetime import date
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsBookingOwnerOrReadOnly, IsLandlordForBooking



class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_renter:
            return Booking.objects.filter(user=user)
        elif user.is_landlord:
            return Booking.objects.filter(listing__owner=user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        print(f"User: {user} (is_authenticated={user.is_authenticated})")
        if not user.is_authenticated:
            raise PermissionDenied("Authentication credentials were not provided.")
        if user.role == 'landlord':
            raise PermissionDenied("Landlords are not allowed to create bookings.")
        serializer.save(user=user)

        listing = serializer.validated_data['listing']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        overlapping = Booking.objects.filter(
            listing=listing,
            status__in=['pending', 'confirmed'],
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

        if overlapping:
            raise serializers.ValidationError("This listing is already booked for the selected dates.")

        serializer.save(user=self.request.user, status='pending')


class BookingCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status not in ['pending', 'confirmed']:
            return Response({"detail": "Booking cannot be cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        if booking.start_date <= date.today():
            return Response({"detail": "Cannot cancel booking on or after start date."}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'cancelled'
        booking.save()
        return Response({"detail": "Booking cancelled successfully."})


class BookingConfirmDeclineView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.listing.owner != request.user:
            return Response({"detail": "You do not have permission to modify this booking."}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action')
        if action not in ['confirm', 'decline']:
            return Response({"detail": "Invalid action. Must be 'confirm' or 'decline'."}, status=status.HTTP_400_BAD_REQUEST)

        if booking.status != 'pending':
            return Response({"detail": "Only pending bookings can be confirmed or declined."}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'confirmed' if action == 'confirm' else 'declined'
        booking.save()
        return Response({"detail": f"Booking {booking.status} successfully."})


# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated, IsBookingOwnerOrReadOnly]
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_renter:
#             return Booking.objects.filter(user=user)
#         elif user.is_landlord:
#             return Booking.objects.filter(listing__owner=user)
#         return Booking.objects.none()




class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookingOwnerOrReadOnly]

    print("BookingViewSet::self.request.user ")

    def get_object(self):
        obj = get_object_or_404(Booking, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        user = self.request.user
        print("BookingViewSet::get_queryset::self.request.user ", user.role)

        if user.is_renter:
            return Booking.objects.filter(user=user)
        elif user.is_landlord:
            return Booking.objects.filter(listing__owner=user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        print(f"Booking creation by user: {user}, role: {user.role}")
        if user.role == 'landlord':
            raise PermissionDenied("Landlords are not allowed to create bookings.")
        serializer.save(user=user)

    def perform_update(self, serializer):
        booking = self.get_object()
        if booking.user != self.request.user:
            raise PermissionDenied("You cannot edit this booking.")
        serializer.save()

    @action(detail=True, methods=['post', 'patch'] , permission_classes=[IsAuthenticated, IsLandlordForBooking])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if booking.status != 'pending':
            return Response({'detail': 'Booking is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'confirmed'
        booking.save()
        return Response({'status': 'Booking confirmed.'})

    @action(detail=True, methods=['post', 'patch'], permission_classes=[IsAuthenticated, IsLandlordForBooking])
    def decline(self, request, pk=None):
        booking = self.get_object()
        if booking.status != 'pending':
            return Response({'detail': 'Booking is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'declined'
        booking.save()
        return Response({'status': 'Booking declined.'})

    @action(detail=True, methods=['post', 'patch'] , permission_classes=[IsAuthenticated, IsBookingOwnerOrReadOnly])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status not in ['pending', 'confirmed']:
            return Response({'detail': 'Cannot cancel this booking.'}, status=status.HTTP_400_BAD_REQUEST)
        if booking.start_date <= date.today():
            return Response({'detail': 'Cannot cancel booking on or after start date.'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'Booking cancelled.'})

class UserBookingsView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(user=user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class BookingStatusUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        booking = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Booking.STATUS_CHOICES).keys():
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = new_status
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)