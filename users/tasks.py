import logging
from celery import shared_task
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.utils import timezone
from django.utils.timezone import now
from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)

class SetLastVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            User.objects.filter(pk=request.user.pk).update(last_login=now())

        return response


@shared_task
def check_and_block_inactive_users():
    """
     Создана асинхронная задача, которая будет выполнять проверку и блокировку пользователей по дате последнего входа:
    """
    logger.info("Checking and blocking inactive users...")
    # Получите текущую дату и вычтите месяц
    one_month_ago = timezone.now() - timedelta(days=30)

    # Найдите пользователей, которые не заходили более месяца и заблокируйте их
    inactive_users = User.objects.filter(last_login__lte=one_month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()@shared_task

    logger.info("Inactive users checked and blocked.")


# celery -A config worker -l INFO
# celery -A config beat -l info -S django

# @shared_task(name="block_inactive_users")
# def check_and_block_inactive_users():
#     print("Check last login user.")
#     need_date = (datetime.today() - timedelta(30)).date()
#     get_users = User.objects.all()
#     print(need_date)
#     for user in get_users:
#         if user.last_login:
#             last = user.last_login.date()
#             print(last)
#             if last < need_date:
#                 print(f"Block user {user.last_login}.")
#                 user.is_active = False
#                 user.save()





