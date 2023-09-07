from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение, позволяющее только владельцу объекта изменять его.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение всегда разрешено, поэтому мы разрешаем GET, HEAD и OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Если запрос на изменение, то проверяем, является ли текущий пользователь владельцем объекта.
        return obj.user_temp == request.user