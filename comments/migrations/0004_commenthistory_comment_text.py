# Generated by Django 5.1.3 on 2024-11-25 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_remove_commenthistory_comment_commenthistory_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commenthistory',
            name='comment_text',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
