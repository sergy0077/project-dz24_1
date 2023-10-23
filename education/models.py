from django.db import models
from config import settings
from users.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


#########################################################################
class Course(models.Model):
    title = models.CharField(max_length=200,  verbose_name='название курса')
    preview = models.ImageField(upload_to='courses/', verbose_name='изображение курса', null=True, blank=True)
    description = models.TextField(verbose_name='описание курса')

    def __str__(self):
        return f"Title: {self.title}, Preview: {self.preview}, Description: {self.description}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

########################################################################
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец урока')
    title = models.CharField(max_length=200,  verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    preview = models.ImageField(upload_to='lessons/', verbose_name='изображение урока', null=True, blank=True)
    video_link = models.URLField( verbose_name='ссылка на видео', null=True, blank=True)

    def __str__(self):
        return f"Title: {self.title}, Course: {self.course}, Owner: {self.owner}, Description: {self.description}, Preview: {self.preview}, Video_link: {self.video_link}"

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

#################################################################

class EducationModeratorGroup(models.Model):
    class Meta:
        verbose_name = "Группа модераторов"
        verbose_name_plural = "Группы модераторов"

    @classmethod
    def create_moderator_group(cls):
        content_type = ContentType.objects.get_for_model(EducationModeratorGroup)
        permission = Permission.objects.create(
            codename='can_manage_courses_and_lessons',
            name='Can manage courses and lessons',
            content_type=content_type,
        )

        group = Group.objects.create(name='Moderators')
        group.permissions.add(permission)

        return group

############################################################################


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='подписка')

    def __str__(self):
        user_email = self.user.email if self.user else 'No User'
        course_title = self.course.title if self.course else 'No Course'
        return f"User: {user_email}, Course: {course_title}, Active: {self.is_active}"
        # return f"User: {self.user.email}, Course: {self.course.title}, Active: {self.is_active}"

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

############################################################################
