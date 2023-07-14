from django.urls import path

from education.apps import EducationConfig
from rest_framework.routers import DefaultRouter

from education.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentsCreateAPIView, PaymentsListAPIView, PaymentsRetrieveAPIView, \
    PaymentsUpdateAPIView, PaymentsDestroyAPIView

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
                  path('payment/create/', PaymentsCreateAPIView.as_view(), name='payment-create'),
                  path('payment/', PaymentsListAPIView.as_view(), name='payment-list'),
                  path('payment/<int:pk>/', PaymentsRetrieveAPIView.as_view(), name='payment-get'),
                  path('payment/update/<int:pk>/', PaymentsUpdateAPIView.as_view(), name='payment-update'),
                  path('payment/delete/<int:pk>/', PaymentsDestroyAPIView.as_view(), name='payment-delete')
              ] + router.urls
