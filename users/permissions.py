from rest_framework.permissions import BasePermission
from users.models import User
from users.models import UserRole

user = User()

# class IsOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user == obj
#
# class IsModerator(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == UserRole.MODERATOR
#
# class IsNotModerator(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role != UserRole.MODERATOR


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == UserRole.MODERATOR:
            return True
        return False
