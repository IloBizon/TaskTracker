# Generated by Django 5.1.3 on 2024-11-23 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_rename_usersprojects_projectuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='update_date',
            new_name='last_update',
        ),
    ]
