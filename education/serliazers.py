from rest_framework import serializers

from education.models import Course, Lesson, Payments

import re


def validate_content(value):
    # Проверка содержимого на наличие недопустимых ссылок
    # В данном случае, разрешаем только ссылки на youtube.com
    pattern = r'(https?://)?(www\.)?youtube\.com'
    if not re.search(pattern, value):
        raise serializers.ValidationError("Содержимое содержит недопустимые ссылки.")
    return value


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

    @staticmethod
    def get_lessons_count(obj):
        """Метод возвращает количество уроков, связанных с курсом."""
        return obj.lessons.count()

    # @staticmethod
    # def get_lesson_data(obj):
    #     lesson_data = []
    #     for lesson in obj.lesson_set.all():
    #         lesson_data.append({
    #             'title': lesson.title,
    #             'description': lesson.description,
    #         })
    #     return lesson_data

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
