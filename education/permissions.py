# from rest_framework.permissions import BasePermission
#
# from education.models import Course
#
#
# class CanModifyCourse(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.groups.filter(name='Модераторы').exists():
#             return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in ['GET', 'PUT', 'PATCH']:
#             return True
#         return False
#
#
# class CanModifyLesson(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.groups.filter(name='Модераторы').exists():
#             return True
#         elif request.method == 'POST':
#             course_id = request.data.get('course')
#             if Course.objects.filter(id=course_id, user=request.user).exists():
#                 return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in ['GET', 'PUT', 'PATCH']:
#             if request.user.groups.filter(name='Модераторы').exists():
#                 return True
#             elif obj.course.user == request.user:
#                 return True
#         return False
