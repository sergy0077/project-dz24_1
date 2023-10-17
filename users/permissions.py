from rest_framework.permissions import BasePermission
from users.models import User
from users.models import UserRole

user = User()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Пользователь имеет доступ, если он является владельцем курса
        return obj.owner == request.user


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        # Пользователь имеет доступ, если он является модератором
        return request.user.role == UserRole.MODERATOR
