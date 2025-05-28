from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from rest_framework import viewsets, permissions
from .permissions import IsOwnerOrReadOnly  # если есть кастомные права


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # возвращаем отзывы для конкретного объявления (получаем id объявления из URL)
        listing_id = self.kwargs.get('listing_id')
        return Review.objects.filter(listing_id=listing_id)

    def perform_create(self, serializer):
        # при создании отзыва автоматически указываем пользователя и объявление
        listing_id = self.kwargs.get('listing_id')
        serializer.save(user=self.request.user, listing_id=listing_id)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
