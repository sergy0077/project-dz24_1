from rest_framework import permissions


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Пользователи могут видеть и редактировать только свои курсы и уроки.
    Модераторы могут видеть и редактировать все курсы и уроки, но не могут их удалять или создавать новые.
    """

    def has_object_permission(self, request, view, obj):
        print(f"User: {request.user}")
        print(f"Lesson owner: {obj.owner}")

        if request.user.groups.filter(name='Moderators').exists():
            # Модераторы могут видеть и редактировать все курсы и уроки
            print("User is a moderator")
            return True

        # Пользователи могут видеть и редактировать только свои курсы и уроки
        print("Checking if user is the owner")
        return obj.owner == request.user

    def has_permission(self, request, view):
        print(f"User: {request.user}")
        if request.user and request.user.groups.filter(name='Moderators').exists():
            # Модераторы имеют доступ к этим действиям
            print("User is a moderator")
            return request.method in permissions.SAFE_METHODS or request.method == 'PATCH'
        # Пользователи имеют доступ только к безопасным методам
        print("User is not a moderator")
        return request.method in permissions.SAFE_METHODS
