from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import User
from .models import Lesson, Course, CourseSubscription
from .serliazers import LessonSerializer


class EducationTestCase(APITestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(
            email='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        # Создание тестового курса
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            content='Содержимое тестового курса',
            preview_image='test_preview.png',
            owner=self.user
        )

        # Создание тестовой подписки
        self.subscription = CourseSubscription.objects.create(
            user=self.user,
            course=self.course,
            is_subscribed=True
        )

    def test_create_lesson(self):
        # Тестирование создания уроков

        url = reverse('education:lesson-create')  # Получение URL для создания урока
        data = {
            'title': 'Тест',
            'description': 'Тест',
            'content': 'https://www.youtube.com/',
            'course': self.course.id  # Использование ID курса, созданного в методе setUp
        }

        response = self.client.post(url, data, format='json')  # Отправка POST-запроса для создания урока

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # Проверка, что код статуса ответа равен 201 (Создан)
        self.assertEqual(Lesson.objects.count(), 1)  # Проверка, что был создан объект урока
        self.assertEqual(Lesson.objects.get().title,
                         'Тест')  # Проверка, что созданный урок имеет правильное название

    def test_update_lesson(self):
        """Тестирование обновления уроков"""

        lesson = Lesson.objects.create(
            title='Test',
            description='Test',
            content='https://www.youtube.com/',
            course=self.course,
            owner=self.user
        )

        url = reverse('education:lesson-update', kwargs={'pk': lesson.pk})
        data = {
            'title': 'Тест',
            'description': 'Тест',
            'content': 'https://www.youtube.com/',
            'course': self.course.pk
        }

        response = self.client.put(url, data=data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], data['title'])
        self.assertEquals(response.data['description'], data['description'])
        self.assertEquals(response.data['content'], data['content'])
        self.assertEquals(response.data['course'], data['course'])

    # def test_delete_lesson(self):
    #     """Тестирование удаления урока"""
    #     lesson = Lesson.objects.create(title='Тест',
    #                                    description='Тест',
    #                                    content='https://www.youtube.com/',
    #                                    preview_image=None,
    #                                    course=self.course,
    #                                    owner=self.user
    #                                    )
    #     url = reverse('education:lesson-delete', kwargs={'pk': lesson.id})
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())

    def test_create_course_subscription(self):
        """Тестирование создания подписки"""
        url = reverse('education:subscribe')
        data = {
            'course_id': self.course.id,
            'content': 'https://www.youtube.com/',
            'title': 'Тест',
            'description': 'Тест'
        }
        response = self.client.post(url, data)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        subscription = CourseSubscription.objects.get(user=self.user, course=self.course)
        self.assertTrue(subscription.is_subscribed)

    def test_delete_course_subscription(self):
        """Тестирование удаления подписки"""
        subscription = CourseSubscription.objects.create(user=self.user, course=self.course, is_subscribed=True)
        url = reverse('education:unsubscribe', kwargs={'pk': subscription.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CourseSubscription.objects.filter(id=subscription.id).exists())
