# Generated by Django 4.0.4 on 2022-05-28 19:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Books', '0008_userbookrelation_comment_disliked_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbookrelation',
            name='comment_disliked',
        ),
        migrations.AddField(
            model_name='userbookrelation',
            name='comment_disliked',
            field=models.ManyToManyField(blank=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='userbookrelation',
            name='comment_liked',
        ),
        migrations.AddField(
            model_name='userbookrelation',
            name='comment_liked',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]