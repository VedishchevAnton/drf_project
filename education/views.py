from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Response
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from education.models import Course, Lesson, Payments, CourseSubscription
from education.paginators import VehiclePaginator
from education.permissions import LessonPermission, CoursePermission
from education.serliazers import CourseSerializer, LessonSerializer, PaymentsSerializer
import stripe


class CourseViewSet(viewsets.ModelViewSet):
    """Viewset for course"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, CoursePermission]
    pagination_class = VehiclePaginator

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user).order_by('id')


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [AllowAny, LessonPermission]

    def perform_create(self, serializer):
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, LessonPermission]
    pagination_class = VehiclePaginator

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user).order_by('id')


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [AllowAny, LessonPermission]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, LessonPermission]

    def get_queryset(self):
        return Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny, LessonPermission]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Метод создания платежа"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем данные о платеже из сериализатора
        payment_data = serializer.validated_data

        # Создаем платеж в Stripe
        stripe.api_key = "pk_test_51NXm18JkCiZgdkS3oaayzptg1BOAlOJG39pgaC" \
                         "4i9dtwJPNciNcmnU4lNXBwWT8tjTwlRUp0fOOH4mO5t4vyO7GK00XoQEVRf9"
        payment_intent = stripe.PaymentIntent.create(
            amount=int(payment_data['payment_amount'] * 100),
            currency="usd",
            payment_method_types=["card"],
            metadata={
                "user_id": request.user.id,
                "course_id": payment_data['paid_course'].id,
                "lesson_id": payment_data['paid_lesson'].id,
            },
        )

        # Сохраняем данные о платеже в базе данных
        payment = serializer.save(
            user=request.user,
            payment_intent_id=payment_intent.id,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Получаем данные о платеже из Stripe
        stripe.api_key = "pk_test_51NXm18JkCiZgdkS3oaayzptg1BOAlOJG39pgaC" \
                         "4i9dtwJPNciNcmnU4lNXBwWT8tjTwlRUp0fOOH4mO5t4vyO7GK00XoQEVRf9"
        payment_intent = stripe.PaymentIntent.retrieve(instance.payment_intent_id)

        # Обновляем статус платежа в базе данных
        instance.status = payment_intent.status
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class CourseSubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class CourseSubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = CourseSubscription.objects.all()
    permission_classes = [AllowAny]
