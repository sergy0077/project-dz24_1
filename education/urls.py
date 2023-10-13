from django.urls import path, re_path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import CourseViewSet, LessonViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView, PaymentListView, EducationModeratorGroupView

app_name = 'education'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')


urlpatterns = [
    *router.urls,
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-retrieve-update-destroy'),
    re_path(r'^education_moderator_group/$', EducationModeratorGroupView.as_view(), name='education_moderator_group'),

    path('payments/', PaymentListView.as_view(), name='payment-list'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('register/', views.RegistrationView.as_view(), name='registration'),  # Регистрация пользователя
]
urlpatterns += router.urls
