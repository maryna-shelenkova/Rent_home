from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать или удалять объект только его владельцу.
    Остальные пользователи могут только просматривать (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsLandlordOrReadOnly(permissions.BasePermission):
    """
    Только арендодатели могут создавать/редактировать объявления.
    Остальные (включая арендаторов и неаутентифицированных) — только просмотр.
    """

    def has_permission(self, request, view):
        # Разрешаем безопасные методы всем (GET и т.п.)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_landlord
