from django.core.management.base import BaseCommand
from education.models import Course

class Command(BaseCommand):
    help = 'Creates initial courses'

    def handle(self, *args, **options):
        Course.objects.create(
            title='Course 1',
            description='Description for Course 1'
            # Добавьте другие поля курса, которые вы хотите установить
        )
        self.stdout.write(self.style.SUCCESS('Courses created successfully.'))
