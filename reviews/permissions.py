from rest_framework import permissions


class IsReviewAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user



class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать объект только его владельцу,
    а для остальных только чтение.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user  # если поле user

