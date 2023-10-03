from django.core.management.base import BaseCommand
from education.models import Payments


class Command(BaseCommand):
    help = 'Creates initial payments'

    def handle(self, *args, **options):
        Payments.objects.create(
            user_id=1,
            payment_date='2023-10-01',
            course_or_lesson_id=1,
            amount=100.00,
            payment_method='cash'
        )
        # Д
        self.stdout.write(self.style.SUCCESS('Payments created successfully.'))
