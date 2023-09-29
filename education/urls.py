from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView

app_name = 'education'

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-retrieve-update-destroy'),
]

urlpatterns += router.urls
