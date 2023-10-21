from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import CourseViewSet, LessonViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView, PaymentListView, \
    EducationModeratorGroupView, SubscriptionViewSet

app_name = 'education'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    *router.urls,

    path('payment/', views.PaymentTemplateView.as_view(), name='payment-template'),
    path('create_payment_view/', views.create_payment_view, name='create_payment_view'),
    path('retrieve_payment/<str:payment_intent_id>/', views.retrieve_payment_view, name='retrieve_payment'),
    path('success/', views.SuccessView.as_view(), name='success'),

    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-retrieve-update-destroy'),
    re_path(r'^education_moderator_group/$', EducationModeratorGroupView.as_view(), name='education_moderator_group'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('register/', views.RegistrationView.as_view(), name='registration'),  # Регистрация пользователя

    path('subscribe_to_course/<int:course_id>/', views.subscribe_to_course, name='subscribe_to_course'),
    path('unsubscribe_from_course/<int:course_id>/', views.unsubscribe_from_course, name='unsubscribe_from_course'),

    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
]

urlpatterns += router.urls

