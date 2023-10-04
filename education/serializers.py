from rest_framework import serializers
from .models import Course, Lesson, Payments


class LessonAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'course',
        )
        depth = 1

    course = serializers.StringRelatedField(source='course.title')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'preview', 'video_link')


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'num_lessons', 'lessons')

    def get_num_lessons(self, obj):
        return obj.lesson_set.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ('id', 'user', 'payment_date', 'course_or_lesson', 'amount', 'payment_method')