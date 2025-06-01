from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReviewViewSet
from reviews.views import ReviewListCreateView


router = DefaultRouter()
router.register(r'', ReviewViewSet)  
urlpatterns = [
    path('', include(router.urls)),
    path('listings/<int:listing_id>/reviews/', ReviewListCreateView.as_view(), name='listing-reviews'),
]



