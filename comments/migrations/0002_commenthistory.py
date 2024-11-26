# Generated by Django 5.1.3 on 2024-11-25 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('historical_record', models.CharField(max_length=100)),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='comments.comment')),
            ],
        ),
    ]