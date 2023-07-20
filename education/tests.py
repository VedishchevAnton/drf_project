from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import User
from .models import Lesson
from .serliazers import LessonSerializer


class EducationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания уроков"""

        url = reverse('lesson-create')
        data = {
            "title": "Test",
            "description": "Test",
            "content": "Test",
            "course": "Test"
        }

        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_lesson(self):
        """Тестирование получения уроков"""

        lesson = Lesson.objects.create(
            title='Test',
            description='Test',
            content='Test',
            course='Test',
            owner=self.user
        )

        url = reverse('lesson-retrieve', kwargs={'pk': lesson.pk})
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, LessonSerializer(lesson).data)

    def test_update_lesson(self):
        """Тестирование обновления уроков"""

        lesson = Lesson.objects.create(
            title='Test',
            description='Test',
            content='Test',
            course='Test',
            owner=self.user
        )

        url = reverse('lesson-update', kwargs={'pk': lesson.pk})
        data = {
            "title": "New Test",
            "description": "New Test",
            "content": "New Test",
            "course": "New Test"
        }

        response = self.client.put(url, data=data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], data['title'])
        self.assertEquals(response.data['description'], data['description'])
        self.assertEquals(response.data['content'], data['content'])
        self.assertEquals(response.data['course'], data['course'])

    def test_delete_lesson(self):
        """Тестирование удаления уроков"""

        lesson = Lesson.objects.create(
            title='Test',
            description='Test',
            content='Test',
            course='Test',
            owner=self.user
        )

        url = reverse('lesson-delete', kwargs={'pk': lesson.pk})
        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=lesson.pk).exists())
