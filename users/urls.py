from django.urls import path
from . import views
from users.apps import UsersConfig
from .views import UserListView, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
