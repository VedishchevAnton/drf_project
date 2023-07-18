from rest_framework.permissions import BasePermission


class ModeratorGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()
