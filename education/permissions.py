from rest_framework.permissions import BasePermission


class LessonPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        elif request.method in ['GET', 'PUT', 'PATCH'] and obj.owner == request.user:
            return True
        else:
            return False


class CoursePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        elif request.method in ['GET', 'PUT', 'PATCH'] and obj.owner == request.user:
            return True
        else:
            return False
