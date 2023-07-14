from django.db import models

from users.models import NULLABLE, User


# Create your models here.
class Course(models.Model):
    """Модель курса"""
    title = models.CharField(max_length=200, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса')
    preview_image = models.ImageField(upload_to='course_previews/', verbose_name='Превью', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    preview_image = models.ImageField(upload_to='lesson_previews/', verbose_name='Превью', **NULLABLE)
    course = models.ForeignKey(Course, default=1, on_delete=models.CASCADE, related_name='lessons',
                               verbose_name='Курс')  # related_name='lessons' задает имя обратной связи для доступа к
    # объектам Lesson из объектов Course.

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

# class Payments(models.Model):
#     choices_payment_method_ = [
#         ('cash', 'Наличные'),
#         ('bank transfer', 'Перевод на счет')
#     ]
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
