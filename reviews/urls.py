from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'', ReviewViewSet)  
urlpatterns = [
    path('', include(router.urls)),
]



