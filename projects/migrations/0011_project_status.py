# Generated by Django 5.1.3 on 2024-11-24 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_alter_projectuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('1', 'Активен'), ('2', 'Архивирован')], default='1', max_length=100),
        ),
    ]
