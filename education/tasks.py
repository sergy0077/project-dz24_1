import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def send_update_notification_email(user_email, course_title):
    """
    отправляет уведомления о обновлениях материалов курса пользователям
    """
    logger.info("Sending email notifications to users...")

    subject = 'Обновление материалов курса'
    message = f'Курс "{course_title}" был обновлен. Проверьте новые материалы!'
    from_email = 'kutsenkosergey@mail.ru'
    recipient_list = [user_email]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,  # Если True, ошибки отправки не будут вызывать исключения
        html_message=None  # Здесь можно указать HTML-разметку для письма
    )

    logger.info("Email notifications sent to users.")



# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = os.getenv('EMAIL_PORT')
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
# EMAIL_MODERATOR = os.getenv('EMAIL_MODERATOR')










