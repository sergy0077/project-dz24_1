from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView, PaymentListView, EducationModeratorGroupView

app_name = 'education'

router = DefaultRouter()
# router.register(r'courses', CourseViewSet)
# router.register(r'lessons', LessonViewSet)
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')


urlpatterns = [
    *router.urls,
    #path('', include(router.urls)),

    #path('courses/', CourseViewSet.as_view(), name='course-list'),
    #path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-retrieve-update-destroy'),
    re_path(r'^education_moderator_group/$', EducationModeratorGroupView.as_view(), name='education_moderator_group'),

    path('payments/', PaymentListView.as_view(), name='payment-list'),
]

urlpatterns += router.urls
