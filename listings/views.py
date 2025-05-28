from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Listing
from .serializers import ListingSerializer
from .filters import ListingFilter
from .permissions import IsOwnerOrReadOnly, IsLandlordOrReadOnly


class ListingViewSet(viewsets.ModelViewSet):
    """
    Основной ViewSet для объявлений.
    - Арендаторы (не владельцы) могут только просматривать.
    - Арендодатели могут создавать и редактировать свои объявления.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsLandlordOrReadOnly]

    # Поиск, фильтрация и сортировка
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ListingFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserListingsView(APIView):
    """
    API для получения всех объявлений текущего пользователя (арендодателя).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        listings = Listing.objects.filter(owner=request.user)
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)





