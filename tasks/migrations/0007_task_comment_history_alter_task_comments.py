# Generated by Django 5.1.3 on 2024-11-25 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_commenthistory'),
        ('tasks', '0006_task_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='comment_history',
            field=models.ManyToManyField(blank=True, related_name='comment_history', to='comments.commenthistory'),
        ),
        migrations.AlterField(
            model_name='task',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments', to='comments.comment'),
        ),
    ]