from rest_framework import viewsets, generics

from education.models import Course, Lesson, Payments
from education.serliazers import CourseSerializer, LessonSerializer, PaymentsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
