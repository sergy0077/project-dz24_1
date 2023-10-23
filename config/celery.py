from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab

from celery import Celery

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-and-block-inactive-users': {
        'task': 'users.tasks.check_and_block_inactive_users',
        'schedule': crontab(minute='0', hour='0'),  # Каждый день в полночь
    },
}

app.conf.timezone = 'UTC'

