from rest_framework import serializers
from .models import Course, Lesson, Payments, Subscription
from education.validators import UrlValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подписки пользователя на курсы.
      ---
    parameters:
      - name: user
        description: Идентификатор пользователя
        required: true
        type: integer
      - name: course
        description: Идентификатор курса
        required: true
        type: integer
    responses:
      201:
        description: Подписка успешно создана
      404:
        description: Пользователь или курс не найден
    """
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
        model = Subscription
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
    """
        Информация о конкретном уроке.
        ---
        parameters:
          - name: title
            description: Название урока
            required: true
            type: string
          - name: description
            description: Описание урока
            required: true
            type: string
          - name: preview
            description: Ссылка на превью урока
            required: true
            type: string
          - name: video_link
            description: Ссылка на видео урока
            required: true
            type: string
          - name: course
            description: Идентификатор курса
            required: true
            type: integer
        responses:
          200:
            description: Информация о уроке
          201:
            description: Созданный урок
          204:
            description: Подтверждение об удалении
          404:
            description: Урок не найден
        """
    course_title = serializers.ReadOnlyField(source='course.title')
    class Meta:
        model = Lesson
        fields = ('pk', 'title', 'description', 'preview', 'video_link', 'course_title')
        course = serializers.StringRelatedField()
        UrlValidator = [UrlValidator(field='url')]


class CourseSerializer(serializers.ModelSerializer):
    """
        Информация о курсе.
        ---
        parameters:
          - name: title
            description: Название курса
            required: true
            type: string
          - name: preview
            description: Ссылка на превью курса
            required: true
            type: string
          - name: description
            description: Описание курса
            required: true
            type: string
        responses:
          200:
            description: Информация о курсе
          201:
            description: Созданный курс
          204:
            description: Подтверждение об удалении
          404:
            description: Курс не найден
        """
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    is_active = SubscriptionSerializer(source='*', read_only=True)

    class Meta:
        model = Course
        fields = ('pk', 'title', 'preview', 'description', 'num_lessons', 'lessons', 'is_active')

    def get_num_lessons(self, obj):
        return obj.lesson_set.count()


class PaymentSerializer(serializers.ModelSerializer):
    """
        Информация о платеже.
        ---
        parameters:
          - name: user
            description: Идентификатор пользователя
            required: true
            type: integer
          - name: payment_date
            description: Дата платежа
            required: true
            type: string
          - name: course_or_lesson
            description: Идентификатор курса или урока
            required: true
            type: integer
          - name: amount
            description: Сумма платежа
            required: true
            type: number
          - name: payment_method
            description: Метод платежа
            required: true
            type: string
        responses:
          200:
            description: Информация о платеже
          201:
            description: Созданный платеж
          204:
            description: Подтверждение об удалении
        """
    class Meta:
        model = Payments
        fields = ('pk', 'user', 'payment_date', 'course_or_lesson', 'amount', 'payment_method')


class PaginatedCourseSerializer(serializers.Serializer):
    """
        Сериализатор для пагинированных данных о курсах.
        ---
        properties:
          - name: count
            description: Общее количество курсов
            type: integer
          - name: next
            description: Ссылка на следующую страницу курсов (если есть)
            type: string
          - name: previous
            description: Ссылка на предыдущую страницу курсов (если есть)
            type: string
          - name: results
            description: Список объектов CourseSerializer
    """
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = CourseSerializer(many=True)


class PaginatedLessonSerializer(serializers.Serializer):
    """
        Сериализатор для пагинированных данных о уроках.
        ---
        properties:
          - name: count
            description: Общее количество уроков
            type: integer
          - name: next
            description: Ссылка на следующую страницу уроков (если есть)
            type: string
          - name: previous
            description: Ссылка на предыдущую страницу уроков (если есть)
            type: string
          - name: results
            description: Список объектов LessonSerializer
    """
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = LessonSerializer(many=True)
