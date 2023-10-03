from django.urls import path
from . import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

]
