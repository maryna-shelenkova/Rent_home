from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date
from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied





class BookingListCreateView(generics.ListCreateAPIView):
    """
    List user's bookings or create a new booking
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Показываем только бронирования текущего пользователя
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Проверяем пересечение дат с уже существующими бронированиями на это жильё
        listing = serializer.validated_data['listing']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        overlapping = Booking.objects.filter(
            listing=listing,
            status__in=['pending', 'confirmed'],  # учитываем только активные бронирования
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

        if overlapping:
            raise serializers.ValidationError("This listing is already booked for the selected dates.")

        serializer.save(user=self.request.user, status='pending')


class BookingCancelView(APIView):
    """
    User cancels their booking (if allowed)
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status not in ['pending', 'confirmed']:
            return Response({"detail": "Booking cannot be cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что бронь не истекла (начало брони в будущем)
        if booking.start_date <= date.today():
            return Response({"detail": "Cannot cancel booking on or after start date."}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'cancelled'
        booking.save()
        return Response({"detail": "Booking cancelled successfully."})


class BookingConfirmDeclineView(APIView):
    """
    Landlord confirms or declines booking
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, что текущий пользователь — владелец объявления
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



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookingOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # Арендатор видит только свои бронирования
        if user.is_renter:
            return Booking.objects.filter(user=user)
        # Арендодатель видит бронирования своих объектов
        elif user.is_landlord:
            return Booking.objects.filter(listing__owner=user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        booking = self.get_object()
        if booking.user != self.request.user:
            raise PermissionDenied("Вы не можете редактировать это бронирование.")
        serializer.save()



class UserBookingsView(APIView):
    permission_classes = [IsAuthenticated]

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