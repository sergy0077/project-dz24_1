from django.core.management.base import BaseCommand
from education.management.commands.create_lessons import Command as CreateLessonsCommand
from education.management.commands.create_courses import Command as CreateCoursesCommand
from education.models import Subscription


class Command(BaseCommand):
    help = 'Creates initial subscriptions'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='The ID of the user for whom the subscription is created')
        parser.add_argument('course_id', type=int, help='The ID of the course to which the subscription belongs')

    def handle(self, *args, **options):
        user_id = options['user_id']
        course_id = options['course_id']
        Subscription.objects.create(
            user_id=user_id,
            course_id=course_id,
            is_active=True
            # Добавьте другие поля подписки, которые вы хотите установить
        )
        self.stdout.write(self.style.SUCCESS('Subscriptions created successfully.'))

    # def handle(self, *args, **options):
    #     # Создаем уроки
    #     create_lessons_command = CreateLessonsCommand()
    #     create_lessons_command.handle()
    #
    #     # Создаем курсы
    #     create_courses_command = CreateCoursesCommand()
    #     create_courses_command.handle()
    #
    #     # Создаем подписки
    #     Subscription.objects.create(
    #         user_id=1,
    #         course_id=1,
    #         is_active=True
    #         # Добавьте другие поля подписки, которые вы хотите установить
    #     )
    #     self.stdout.write(self.style.SUCCESS('Subscriptions created successfully.'))
