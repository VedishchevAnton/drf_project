from django.db import models

from users.models import NULLABLE


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
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
