# Generated by Django 4.2.6 on 2023-10-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0009_lesson_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=200, verbose_name='название курса'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='title',
            field=models.CharField(max_length=200, verbose_name='название урока'),
        ),
    ]
