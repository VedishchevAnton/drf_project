from rest_framework import serializers

from education.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()  # Определение дополнительного поля lesson_count с помощью
    # SerializerMethodField(). Это поле будет возвращать количество уроков, связанных с курсом.

    @staticmethod
    def get_lesson_count(obj):
        """Метод возвращает количество уроков, связанных с курсом."""
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview_image', 'lesson_count']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
