# Generated by Django 5.1.3 on 2024-11-24 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_projecthistory_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectuser',
            name='role',
            field=models.CharField(choices=[(1, 'Младший специалист'), (2, 'Специалист'), (3, 'Ведущий специалист'), (4, 'Главный специалист'), (5, 'Руководитель проекта')], max_length=100),
        ),
    ]
