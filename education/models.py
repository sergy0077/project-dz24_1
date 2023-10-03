from django.db import models
from config import settings
from users.models import User

################################################################
class Course(models.Model):
    title = models.CharField(max_length=200,  verbose_name='развание курса')
    preview = models.ImageField(upload_to='courses/', verbose_name='изображение курса', null=True, blank=True)
    description = models.TextField(verbose_name='описание курса')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

########################################################################
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    title = models.CharField(max_length=200,  verbose_name='Название урока')
    description = models.TextField(verbose_name='описание урока')
    preview = models.ImageField(upload_to='lessons/', verbose_name='изображение урока', null=True, blank=True)
    video_link = models.URLField( verbose_name='ссылка на видео', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

###########################################################################
class Payments(models .Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    payment_date = models.DateField(verbose_name='дата оплаты')
    course_or_lesson = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    CASH = 'cash'
    TRANSFER = 'transfer'
    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Cash'),
        (TRANSFER, 'Transfer'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f"Payment for {self.course_or_lesson} by {self.user} on {self.payment_date}"

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
