from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson, Payments
from education.permissions import CanModifyCourse, CanModifyLesson
from education.serliazers import CourseSerializer, LessonSerializer, PaymentsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, CanModifyCourse]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, CanModifyLesson]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, CanModifyLesson]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(course__user=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, CanModifyLesson]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(course__user=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, CanModifyLesson]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(course__user=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, CanModifyLesson]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')  # Набор полей для фильтрации
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated]


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]
