# Generated by Django 4.2.6 on 2023-10-22 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fullname',
        ),
    ]
