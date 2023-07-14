from rest_framework import serializers

from education.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()  # Определение дополнительного поля lesson_count с помощью

    # SerializerMethodField(). Это поле будет возвращать количество уроков, связанных с курсом.
    lessons = LessonSerializer(many=True,
                               read_only=True)  # Параметр many=True указывает, что поле lessons является коллекцией
    # объектов, а read_only=True означает, что это поле только для чтения и не будет использоваться для создания или
    # обновления объектов

    @staticmethod
    def get_lesson_count(obj):
        """Метод возвращает количество уроков, связанных с курсом."""
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'
