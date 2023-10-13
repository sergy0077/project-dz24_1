from django.http import HttpResponse
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions
from .permissions import IsOwnerOrModerator
from .models import Course, Lesson, Payments
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from django_filters import rest_framework as filters
from .filters import PaymentFilter
from rest_framework.filters import OrderingFilter

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from users.serializers import UserSerializer


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


