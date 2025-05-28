from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookingViewSet,
    BookingListCreateView,
    UserBookingsView,
    BookingStatusUpdateView,
    BookingCancelView,
    BookingConfirmDeclineView,
)

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Роутер с ViewSet
    path('list/', BookingListCreateView.as_view(), name='booking-list-create'),  # отдельный листинг
    path('my-bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('<int:pk>/status/', BookingStatusUpdateView.as_view(), name='booking-status-update'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
    path('<int:pk>/confirm-decline/', BookingConfirmDeclineView.as_view(), name='booking-confirm-decline'),
]





