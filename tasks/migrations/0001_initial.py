# Generated by Django 5.1.3 on 2024-11-25 11:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0012_remove_project_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('status', models.CharField(choices=[('PREP', 'Подготовка'), ('PROG', 'В процессе'), ('DONE', 'Выполнено')], max_length=100)),
                ('priority', models.CharField(choices=[('1', 'Низкий'), ('2', 'Средний'), ('3', 'Высокий')], max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(null=True)),
                ('due_date', models.DateTimeField(null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='projects.project')),
                ('testing_responsible', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='testing_responsible', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
