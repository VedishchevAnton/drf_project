from celery import shared_task
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from drf_project import settings
from education.models import Course, CourseSubscription


@shared_task
def send_course_update(course_id):
    try:
        course = Course.objects.get(pk=course_id)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['vedishchevanton@gmail.com']
        subject = f"Обновление курса {course.title}"
        message = f"Курс {course.title} был обновлен. Проверьте новый контент на сайте."
        send_mail(subject, message, from_email, recipient_list=recipient_list, fail_silently=False)
    except Course.DoesNotExist:
        print(f"Курс с id {course_id} не найден.")
