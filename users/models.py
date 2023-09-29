from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(models.Model):
    username = models.CharField(max_length=150, verbose_name='имя пользователя', null=True)
    fullname = models.CharField(max_length=150, verbose_name='ФИ0')
    email = models.EmailField(max_length=150, verbose_name='почта', unique=True)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='город')
    avatar = models.ImageField(upload_to='avatar/', verbose_name='аватарка', null=True, blank=True)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
