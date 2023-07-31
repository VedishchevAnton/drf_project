from celery import shared_task

from django.core.mail import send_mail
from django.utils import timezone

from drf_project import settings
from education.models import Course, CourseSubscription
from users.models import User


@shared_task
def send_course_update(course_id):
    """Метод рассылки информации об обновлении курса"""
    try:
        course = Course.objects.get(pk=course_id)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['vedishchevanton@gmail.com']
        subject = f"Обновление курса {course.title}"
        message = f"Курс {course.title} был обновлен. Проверьте новый контент на сайте."
        send_mail(subject, message, from_email, recipient_list=recipient_list, fail_silently=False)
    except Course.DoesNotExist:
        print(f"Курс с id {course_id} не найден.")


@shared_task
def block_inactive_users():
    """Метод блокировки пользователей, которые не заходили более месяца"""
    one_month_ago = timezone.now() - timezone.timedelta(days=30)  # Получаем дату, которая была месяц назад
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago)   # Получаем пользователей, которые не заходили более месяца
    inactive_users.update(is_active=False)  # Блокируем пользователей
