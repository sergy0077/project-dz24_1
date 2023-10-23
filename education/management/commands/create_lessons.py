from django.core.management.base import BaseCommand
from education.models import Lesson


class Command(BaseCommand):
    help = 'Creates initial lessons'

    def add_arguments(self, parser):
        parser.add_argument('course_id', type=int, help='The ID of the course to which the lesson belongs')

    def handle(self, *args, **options):
        course_id = options['course_id']
        Lesson.objects.create(
            course_id=course_id,
            owner_id=1,
            title='Lesson 1',
            description='Description for Lesson 1'
            # Добавьте другие поля урока, которые вы хотите установить
        )
        self.stdout.write(self.style.SUCCESS('Lessons created successfully.'))
