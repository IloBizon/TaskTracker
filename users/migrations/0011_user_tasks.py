# Generated by Django 5.1.3 on 2024-11-25 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        ('users', '0010_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tasks',
            field=models.ManyToManyField(to='tasks.task'),
        ),
    ]
