from django.db import models
from django.utils import timezone

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


class Payments(models.Model):
    choices_payment_method = [
        ('cash', 'Наличные'),
        ('bank transfer', 'Перевод на счет')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(default=timezone.now, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='paid_course',
                                    verbose_name='Оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='paid_lesson',
                                    verbose_name='Оплаченный урок', **NULLABLE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name='Сумма оплаты')  # модель DecimalField позволяет хранить
    # Десятичные числа с фиксированной точностью. Максимальное количество цифр(max_digits), которое может быть
    # хранено, равно 10, а количество знаков(decimal_places) после запятой равно 2.
    payment_method = models.CharField(max_length=20, choices=choices_payment_method, verbose_name='Метод оплаты')

    def __str__(self):
        return f"{self.user} - {self.paid_course or self.paid_lesson} - {self.payment_method}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
