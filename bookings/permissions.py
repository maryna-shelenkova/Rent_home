from rest_framework import permissions

class IsBookingOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsLandlordForBooking(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.listing.owner == request.user



class IsRenter(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'renter'

class IsRenterForCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.role == 'renter'
        return True