from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

NULLABLE = {'blank': True, 'null': True}


class UserRole(models.TextChoices):
    MODERATOR = 'moderator'
    MEMBER = 'member'


class User(AbstractUser):
    username = models.CharField(max_length=150, verbose_name='имя пользователя', null=True)
    email = models.EmailField(max_length=150, verbose_name='почта', unique=True)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='город')
    last_visit = models.DateTimeField(max_length=150, verbose_name='последнее посещение')
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.MEMBER)
    group = models.ManyToManyField('auth.Group', blank=True, related_name='custom_users_group')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} ({self.email}), Phone: {self.phone}, City: {self.city}"
