from django.http import HttpResponse
from django.views import View
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


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrModerator]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator]
        return super(CourseViewSet, self).get_permissions()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrModerator]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator]
        return super(LessonViewSet, self).get_permissions()


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class CoursePagination(PageNumberPagination):
    page_size = 10 # количество элементов на странице


class LessonPagination(PageNumberPagination):
    page_size = 10  # количество элементов на странице


class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = PaginatedCourseSerializer
    pagination_class = CoursePagination


class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = PaginatedLessonSerializer
    pagination_class = LessonPagination


class PaymentFilterView(filters.FilterSet):
    class Meta:
        model = Payments
        fields = {
            'payment_date': ['exact', 'lte', 'gte'],
            'course_or_lesson': ['exact'],
            'payment_method': ['exact'],
        }


class PaymentListView(generics.ListCreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter
    filterset_fields = ('payment_date__gte', 'payment_date__lte', 'course_or_lesson', 'payment_method')  # Набор полей для фильтрации


class EducationModeratorGroupView(View):
    def get(self, request, *args, **kwargs):
        # Ваша логика обработки GET-запроса
        return HttpResponse("Hello, Education Moderator Group!")

####################################################


class RegistrationView(generics.CreateAPIView):
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
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


@api_view(['POST'])
def subscribe_to_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    user = request.user
    subscription = Subscription.objects.create(user=user, course=course)
    return Response({'message': 'Successfully subscribed to the course.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def unsubscribe_from_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscription = Subscription.objects.get(user=request.user, course=course)
        subscription.delete()
        return Response({'message': 'Successfully unsubscribed from the course.'}, status=status.HTTP_204_NO_CONTENT)
    except (Course.DoesNotExist, Subscription.DoesNotExist):
        return Response({'message': 'Course or subscription not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def lesson_detail(request, course_id, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id, course_id=course_id)
        # ... ваш код ...
        return Response(data, status=status.HTTP_200_OK)
    except Lesson.DoesNotExist:
        return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


##############################################################################