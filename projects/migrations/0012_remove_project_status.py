# Generated by Django 5.1.3 on 2024-11-24 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_project_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='status',
        ),
    ]
