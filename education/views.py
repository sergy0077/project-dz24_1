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
# from django.shortcuts import render
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
#
# from lesson.models import Lesson
# from lesson.serializers import LessonSerializer
# from users.permissions import IsNotModerator, IsOwner, IsModerator
#
#
# class LessonCreateAPIView(generics.CreateAPIView):
#     serializer_class = LessonSerializer
#     permission_classes = [IsAuthenticated | IsNotModerator]
#
#     def perform_create(self, serializer):
#         lesson = serializer.save()
#         lesson.owner = self.request.user
#         lesson.save()
#
#
# class LessonListAPIView(generics.ListAPIView):
#     serializer_class = LessonSerializer
#     queryset = Lesson.objects.all()
#     permission_classes = [IsAuthenticated, IsModerator]
#
#
# class LessonRetrieveAPIView(generics.RetrieveAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#     permission_classes = [IsOwner]
#     lookup_field = 'id'
#
#
# class LessonUpdateAPIView(generics.UpdateAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#     permission_classes = [IsOwner]
#     lookup_field = 'id'
#
#
# class LessonDestroyAPIView(generics.DestroyAPIView):
#     queryset = Lesson.objects.all()
#     permission_classes = [IsOwner | IsNotModerator]
#     lookup_field = 'id'

