from rest_framework import permissions

class IsOwnerOrModerator(permissions.BasePermission):
    """
    Пользователи могут видеть и редактировать только свои курсы и уроки.
    Модераторы могут видеть и редактировать все курсы и уроки, но не могут их удалять или создавать новые.
    """

    def has_object_permission(self, request, view, obj):

        if request.user.groups.filter(name='Moderators').exists():
            # Модераторы могут видеть и редактировать все курсы и уроки
            return True

        # Пользователи могут видеть и редактировать только свои курсы и уроки
        return obj.user == request.user

    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Moderators').exists():
            # Модераторы имеют доступ к этим действиям
            return request.method in permissions.SAFE_METHODS or request.method == 'PATCH'
        # Пользователи имеют доступ только к безопасным методам
        return request.method in permissions.SAFE_METHODS
