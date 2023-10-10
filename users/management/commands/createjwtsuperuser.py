from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser with JWT authentication'

    def handle(self, *args, **options):
        User = get_user_model()
        email = input('Enter email: ')
        password = input('Enter password: ')

        # Перед созданием суперпользователя, вы можете установить username в None
        user = User(email=email, username=None)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))