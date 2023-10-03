import django_filters
from .models import Payments


class PaymentFilter(django_filters.FilterSet):

    # Фильтр по дате оплаты больше или равно
    payment_date__gte = django_filters.DateFilter(field_name='payment_date', lookup_expr='gte')

    # Фильтр по дате оплаты меньше или равно
    payment_date__lte = django_filters.DateFilter(field_name='payment_date', lookup_expr='lte')

    # фильтр по курсу или уроку
    course_or_lesson = django_filters.NumberFilter(field_name='course_or_lesson')

    # фильтр по способу оплаты
    payment_method = django_filters.ChoiceFilter(field_name='payment_method', choices=Payments.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payments
        fields = ['payment_date__gte', 'payment_date__lte', 'course_or_lesson', 'payment_method']
