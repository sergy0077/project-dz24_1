import stripe
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.templatetags.rest_framework import data
from .filters import PaymentFilter
from .permissions import IsOwnerOrModerator
from .models import Course, Lesson, Payments, Subscription, User
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from users.serializers import UserSerializer
from rest_framework import viewsets, generics, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .serializers import PaginatedCourseSerializer, PaginatedLessonSerializer
from django.http import JsonResponse
from .stripe_helpers import create_payment_intent, retrieve_payment_intent
from django.views.generic import TemplateView


class CourseViewSet(viewsets.ModelViewSet):
    """
       Управление курсами.
       ---
       parameters:
         - name: course_id
           description: Идентификатор курса
           required: true
           type: integer
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
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrModerator]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator]
        return super(CourseViewSet, self).get_permissions()


class LessonViewSet(viewsets.ModelViewSet):
    """
       Управление уроками.
       ---
       parameters:
         - name: lesson_id
           description: Идентификатор урока
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
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrModerator]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator]
        return super(LessonViewSet, self).get_permissions()


class LessonListCreateView(generics.ListCreateAPIView):
    """
        Получение списка уроков и создание нового урока.
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
            description: Список уроков
          201:
            description: Урок успешно создан
        """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
        Получение, обновление и удаление урока.
        ---
        parameters:
          - name: pk
            description: Идентификатор урока
            required: true
            type: integer
        responses:
          200:
            description: Информация об уроке
          204:
            description: Урок успешно удален
          404:
            description: Урок не найден
        """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

##########################################################################
class CoursePagination(PageNumberPagination):
    """
       Пагинация для списка курсов.
    """
    page_size = 10 # количество элементов на странице


class LessonPagination(PageNumberPagination):
    """
       Пагинация для списка уроков.
    """
    page_size = 10  # количество элементов на странице

###########################################################################
class CourseListView(ListAPIView):
    """
        Получение списка курсов.
        ---
        parameters:
          - name: page
            description: Номер страницы
            required: false
            type: integer
        responses:
          200:
            description: Список курсов
    """
    queryset = Course.objects.all()
    serializer_class = PaginatedCourseSerializer
    pagination_class = CoursePagination


class LessonListView(ListAPIView):
    """
        Получение списка уроков.
        ---
        parameters:
          - name: page
            description: Номер страницы
            required: false
            type: integer
        responses:
          200:
            description: Список уроков
    """
    queryset = Lesson.objects.all()
    serializer_class = PaginatedLessonSerializer
    pagination_class = LessonPagination

#############################################################################

class PaymentFilterView(filters.FilterSet):
    """
       Фильтрация платежей по дате, курсу/уроку и методу платежа.
    """
    class Meta:
        model = Payments
        fields = {
            'payment_date': ['exact', 'lte', 'gte'],
            'course_or_lesson': ['exact'],
            'payment_method': ['exact'],
        }


class PaymentTemplateView(TemplateView):
    template_name = 'education/payment.html'


class SuccessView(TemplateView):
    template_name = 'education/success.html'


class PaymentListView(generics.ListCreateAPIView):
    """
        Получение списка платежей или создание нового платежа.
        ---
        parameters:
          - name: payment_date__gte
            description: Начальная дата платежа (включительно)
            required: false
            type: string
          - name: payment_date__lte
            description: Конечная дата платежа (включительно)
            required: false
            type: string
          - name: course_or_lesson
            description: Идентификатор курса или урока
            required: false
            type: integer
          - name: payment_method
            description: Метод платежа
            required: false
            type: string
        responses:
          200:
            description: Список платежей
          201:
            description: Созданный платеж
        """
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter
    filterset_fields = ('payment_date__gte', 'payment_date__lte', 'course_or_lesson', 'payment_method')  # Набор полей для фильтрации


stripe.api_key = 'sk_test_51O32tgHJsK4c6F7ofMOFM8hrX74oxpqjAm1zfUUa1MghPDWtLb2v3ANJimndQ8LtCpllOOGgRaZXJlkMEMy8i9V200rDlEyJYw'

@csrf_exempt
def create_payment_view(request):
    print(request.POST)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method=payment_method,
                confirm=True,
            )

            return JsonResponse({'client_secret': intent.client_secret})
        except stripe.error.CardError as e:
            return JsonResponse({'error': str(e.error.message)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def retrieve_payment_view(request, payment_intent_id):
    try:
        payment_intent = retrieve_payment_intent(payment_intent_id)
        return JsonResponse({'status': payment_intent.status})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

###################################################################################################################################

class EducationModeratorGroupView(View):
    """
       Представление для модераторов образования.
       ---
       responses:
         200:
           description: Успешный ответ с сообщением
    """
    def get(self, request, *args, **kwargs):
        # Ваша логика обработки GET-запроса
        return HttpResponse("Hello, Education Moderator Group!")

####################################################


class RegistrationView(generics.CreateAPIView):
    """
        Регистрация нового пользователя.
        ---
        parameters:
          - name: username
            description: Имя пользователя
            required: true
            type: string
          - name: email
            description: Электронная почта пользователя
            required: true
            type: string
          - name: password
            description: Пароль пользователя
            required: true
            type: string
        responses:
          201:
            description: Пользователь успешно зарегистрирован
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        refresh = RefreshToken.for_user(user)  # Генерация токенов
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)

####################################################################################


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
        Управление подписками пользователей на курсы.
        ---
        responses:
          200:
            description: Успешный ответ с данными подписки
    """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


@api_view(['POST'])
def subscribe_to_course(request, course_id):
    """
        Подписка пользователя на курс.
        ---
        parameters:
          - name: course_id
            description: Идентификатор курса
            required: true
            type: integer
        responses:
          201:
            description: Подписка успешно создана
          404:
            description: Курс не найден
    """
    course = Course.objects.get(pk=course_id)
    user = request.user
    subscription = Subscription.objects.create(user=user, course=course)
    return Response({'message': 'Successfully subscribed to the course.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def unsubscribe_from_course(request, course_id):
    """
        Отписка пользователя от курса.
        ---
        parameters:
          - name: course_id
            description: Идентификатор курса
            required: true
            type: integer
        responses:
          204:
            description: Успешный ответ с сообщением
          404:
            description: Курс или подписка не найдены
    """
    try:
        course = Course.objects.get(id=course_id)
        subscription = Subscription.objects.get(user=request.user, course=course)
        subscription.delete()
        return Response({'message': 'Successfully unsubscribed from the course.'}, status=status.HTTP_204_NO_CONTENT)
    except (Course.DoesNotExist, Subscription.DoesNotExist):
        return Response({'message': 'Course or subscription not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def lesson_detail(request, course_id, lesson_id):
    """
       Получение информации о конкретном уроке в рамках курса.
       ---
       parameters:
         - name: course_id
           description: Идентификатор курса
           required: true
           type: integer
         - name: lesson_id
           description: Идентификатор урока
           required: true
           type: integer
       responses:
         200:
           description: Информация о уроке
         404:
           description: Урок не найден
       """
    try:
        lesson = Lesson.objects.get(id=lesson_id, course_id=course_id)
        return Response(data, status=status.HTTP_200_OK)
    except Lesson.DoesNotExist:
        return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


##############################################################################