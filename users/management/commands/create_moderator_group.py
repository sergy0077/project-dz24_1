from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from education.models import Course, Lesson  # Замените education на имя вашего приложения


class Command(BaseCommand):
    help = 'Create a moderator group with specific permissions'

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(name='Модераторы')

        # Получаем разрешения для изменения и просмотра курсов и уроков
        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)

        change_course_permission = Permission.objects.get(content_type=course_content_type, codename='change_course')
        view_course_permission = Permission.objects.get(content_type=course_content_type, codename='view_course')
        change_lesson_permission = Permission.objects.get(content_type=lesson_content_type, codename='change_lesson')
        view_lesson_permission = Permission.objects.get(content_type=lesson_content_type, codename='view_lesson')

        # Назначаем разрешения группе модераторов
        moderator_group.permissions.add(change_course_permission, view_course_permission,
                                         change_lesson_permission, view_lesson_permission)

        self.stdout.write(self.style.SUCCESS('Moderator group created successfully'))
