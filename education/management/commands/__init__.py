from education.management.commands.create_lessons import Command as CreateLessonsCommand
from education.management.commands.create_courses import Command as CreateCoursesCommand
from education.management.commands.create_subscriptions import Command as CreateSubscriptionsCommand
from education.management.commands.create_payments import Command as CreatePaymentCommand

__all__ = [
    'CreateLessonsCommand',
    'CreateCoursesCommand',
    'CreateSubscriptionsCommand',
    'CreatePaymentCommand',
    # Добавьте другие команды, если есть
]
