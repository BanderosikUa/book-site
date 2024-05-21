# Generated by Django 4.0.4 on 2024-05-21 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('authors', '0001_initial'),
        ('genres', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbookrelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentbook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book'),
        ),
        migrations.AddField(
            model_name='commentbook',
            name='disliked',
            field=models.ManyToManyField(blank=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentbook',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentbook',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_author', to='authors.author'),
        ),
        migrations.AddField(
            model_name='book',
            name='comments',
            field=models.ManyToManyField(related_name='comments', through='books.CommentBook', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='book_genres', to='genres.genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='readers',
            field=models.ManyToManyField(related_name='books', through='books.UserBookRelation', to=settings.AUTH_USER_MODEL),
        ),
    ]
