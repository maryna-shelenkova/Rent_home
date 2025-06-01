from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, UserListingsView
from reviews.views import ReviewListCreateView


router = DefaultRouter()
router.register(r'', ListingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my-listings/', UserListingsView.as_view(), name='my-listings'),
    path('listings/<int:listing_id>/reviews/', ReviewListCreateView.as_view(), name='listing-reviews'),
]
