from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200,  verbose_name='Название курса')
    preview = models.ImageField(upload_to='previews/', verbose_name='превью', null=True, blank=True)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200,  verbose_name='Название урока')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='превью', null=True, blank=True)
    video_link = models.URLField( verbose_name='ссылка на видео')

    def __str__(self):
        return self.title
