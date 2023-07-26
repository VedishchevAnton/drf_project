from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from drf_project import settings
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


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')  # Набор полей для фильтрации
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated]


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()  # запрос на получение всех объектов модели Payments
    permission_classes = [IsAuthenticated]  # классы разрешений, необходимых для доступа к представлению


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


class PaymentsCreateIntentAPIView(generics.CreateAPIView):
    """Cоздание платежа в Stripe и сохранять его ID"""
    serializer_class = PaymentsSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем данные о платеже из сериализатора
        user = serializer.validated_data.get('user')
        payment_amount = serializer.validated_data.get('payment_amount')
        payment_method = serializer.validated_data.get('payment_method')

        # Создаем платеж в Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=int(payment_amount * 100),  # Сумма платежа в копейках
            currency='rub',  # Валюта платежа
            payment_method=payment_method,  # Метод оплаты
            confirmation_method='manual',  # Ручное подтверждение платежа
            confirm=True,  # Автоматически подтверждать платеж
        )

        # Сохраняем ID платежа в модели Payments
        payment = Payments.objects.create(
            user=user,
            payment_amount=payment_amount,
            payment_method=payment_method,
            payment_intent_id=intent.id,
        )

        # Возвращаем данные о платеже в ответе
        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentsRetrieveIntentAPIView(generics.RetrieveAPIView):
    """Получение данныx о платеже из Stripe и обновлять статус платежа"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Получаем данные о платеже из Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.retrieve(instance.payment_intent_id)

        # Обновляем статус платежа в модели Payments
        instance.payment_status = intent.status
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
