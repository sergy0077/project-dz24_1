from rest_framework import serializers
from .models import Course, Lesson, Payments, Subscription
from education.validators import UrlValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    def get_subscription_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            course = obj
            user = request.user
            try:
                subscription = Subscription.objects.get(user=user, course=course)
                return True
            except Subscription.DoesNotExist:
                return False
        return False

    class Meta:
        model: Subscription
        fields = (
            'user',
            'course',
            'is_active',
        )


class LessonAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('pk', 'title', 'course')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('pk', 'title', 'description', 'preview', 'video_link')
        course = serializers.StringRelatedField()
        UrlValidator = [UrlValidator(field='url')]


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    is_active = SubscriptionSerializer(source='*', read_only=True)

    class Meta:
        model = Course
        fields = ('pk', 'title', 'preview', 'description', 'num_lessons', 'lessons')

    def get_num_lessons(self, obj):
        return obj.lesson_set.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ('pk', 'user', 'payment_date', 'course_or_lesson', 'amount', 'payment_method')


class PaginatedCourseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = CourseSerializer(many=True)


class PaginatedLessonSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = LessonSerializer(many=True)
