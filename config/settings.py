"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&*$jo4=qv$7=f$ns*6hl#o%t)k^so6c6(zf2%6v@y&2=l-$2dk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',

    'rest_framework',
    'rest_framework_simplejwt',

    'rest_framework.authtoken',
    'drf_yasg',
    'corsheaders',
    'django_filters',

    'users',
    'education',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'users.tasks.SetLastVisitMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'users', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'project_24_1',
        'USER': 'postgres',
        'PASSWORD': '130468',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "education/static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    # Настройки JWT-токенов
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Настройки срока действия токенов
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  # Разрешенный локальный источник
    "https://example.com",    # Разрешенный источник
]
CORS_ALLOW_ALL_ORIGINS = True

STRIPE_PUBLIC_KEY = 'pk_test_51O32tgHJsK4c6F7oUI99Pq5BD7j4kIvY3xeDtz5gKNWsnl6VVYxLiKfaBsWZ39W5fYBffZufjluyzzvafryYFWBA00bWNJwgh3'
STRIPE_SECRET_KEY = 'sk_test_51O32tgHJsK4c6F7ofMOFM8hrX74oxpqjAm1zfUUa1MghPDWtLb2v3ANJimndQ8LtCpllOOGgRaZXJlkMEMy8i9V200rDlEyJYw'

# Настройки для Celery

# URL-адрес брокера сообщений
CELERY_BROKER_URL = 'redis://localhost:6379' # Например, Redis, который по умолчанию работает на порту 6379
# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# Часовой пояс для работы Celery
CELERY_TIMEZONE = "UTC"
# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True
# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {
    'tasks': {
        'task': 'education.tasks',  # Путь к вашей асинхронной задаче
        'schedule': crontab(minute='0', hour='0'),  # Расписание выполнения задачи (здесь ежедневно в полночь)
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'ваш_smtp_сервер'
EMAIL_PORT = 587  # Порт вашего SMTP-сервера (обычно 587 для TLS)
EMAIL_USE_TLS = True  # Использовать TLS (если True) или SSL (если False)
EMAIL_HOST_USER = 'ваш_email@example.com'  # Ваша электронная почта
EMAIL_HOST_PASSWORD = 'ваш_пароль'  # Ваш пароль к почтовому ящику
DEFAULT_FROM_EMAIL = 'ваш_email@example.com'  # Email-адрес отправителя по умолчанию

