# Generated by Django 5.1.3 on 2024-11-24 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar_default.png', upload_to='user_avatars'),
        ),
    ]
