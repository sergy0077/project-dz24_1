from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from .models import Course, Lesson, Payments
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from django_filters import rest_framework as filters
from .filters import PaymentFilter
from rest_framework.filters import OrderingFilter


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


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

