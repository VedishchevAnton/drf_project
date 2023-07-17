from rest_framework.permissions import BasePermission


class CanModify(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'PATCH']:
            return True
        return False
