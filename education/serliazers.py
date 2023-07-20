from rest_framework import serializers

from education.models import Course, Lesson, Payments, CourseSubscription

import re

from education.validators import validate_content


class LessonSerializer(serializers.ModelSerializer):
    content = serializers.CharField(validators=[validate_content])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()  # Определение дополнительного поля lesson_count с помощью
    # SerializerMethodField(). Это поле будет возвращать количество уроков, связанных с курсом.
    lessons = LessonSerializer(many=True,
                               read_only=True)  # Параметр many=True указывает, что поле lessons является

    # коллекцией объектов, а read_only=True означает, что это поле только для чтения и не будет использоваться для
    # создания или обновления объектов
    content = serializers.CharField(validators=[validate_content])
    is_subscribed = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(obj):
        """Метод возвращает количество уроков, связанных с курсом."""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Метод проверяет, авторизован ли текущий пользователь и подписан ли он на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CourseSubscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
