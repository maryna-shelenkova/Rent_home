from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Listing
from .serializers import ListingSerializer
from .filters import ListingFilter
from .permissions import IsOwnerOrReadOnly, IsLandlordOrReadOnly
from rest_framework.decorators import action
from rest_framework import status
from .permissions import IsLandlordOrReadOnly



class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsLandlordOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ListingFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'id']

    def get_queryset(self):
        user = self.request.user
        queryset = Listing.objects.all()
        if not user.is_authenticated or getattr(user, "is_renter", False):
            return queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsLandlordOrReadOnly])
    def toggle_active(self, request, pk=None):
        listing = self.get_object()
        listing.is_active = not listing.is_active
        listing.save()
        return Response({'status': 'updated', 'is_active': listing.is_active}, status=status.HTTP_200_OK)


class UserListingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        listings = Listing.objects.filter(owner=request.user)
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)





