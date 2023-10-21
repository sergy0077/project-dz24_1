from rest_framework import generics, viewsets, permissions
from education.permissions import IsOwnerOrModerator
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .serializers import UserSerializer


class UserListView(generics.ListCreateAPIView):
    """
       Получение списка всех пользователей или создание нового пользователя.
       ---
       parameters:
         - name: username
           description: Имя пользователя
           required: true
           type: string
       responses:
         200:
           description: Список пользователей
         201:
           description: Созданный пользователь
       """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        Получение, обновление или удаление информации о пользователе.
        ---
        parameters:
          - name: user_id
            description: Идентификатор пользователя
            required: true
            type: integer
        responses:
          200:
            description: Информация о пользователе
          204:
            description: Подтверждение об удалении
          404:
            description: Пользователь не найден
        """
    queryset = User.objects.all()
    serializer_class = UserSerializer


def register(request):
    """
    Представление для регистрации пользователя
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Автоматически входит в систему после регистрации
            return redirect('users:home')  # Перенаправляем на страницу home (замените на вашу целевую страницу)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login(request):
    """
    Представление для входа пользователя
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Автоматически входит в систему после входа
            return redirect('users:home')  # Перенаправляем на страницу home (замените на вашу целевую страницу)
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})



@login_required
def home(request):
    """
    Представление для защищенной страницы
    """
    return render(request, 'users/home.html')

def index(request):
    return render(request, 'index.html', {'message': 'Добро пожаловать на наш сайт!'})