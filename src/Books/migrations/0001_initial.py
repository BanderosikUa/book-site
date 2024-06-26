# Generated by Django 4.0.4 on 2024-05-21 12:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hitcount.models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='No more 255 chars', max_length=255, validators=[django.core.validators.ProhibitNullCharactersValidator])),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')])),
                ('about', models.TextField(blank=True)),
                ('photo', models.ImageField(default='default/book/default_book_cover_2015.jpg', upload_to='books/%Y/%m/%d/')),
                ('author_is_user', models.BooleanField(default=False)),
                ('age_category', models.CharField(choices=[('12', '12+'), ('14', '14+'), ('16', '16+'), ('18', '18+')], default='12', max_length=3)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-hit_count_generic__hits'],
            },
            bases=(models.Model, hitcount.models.HitCountMixin),
        ),
        migrations.CreateModel(
            name='CommentBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=800)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserBookRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmarks', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Plan to read'), (2, 'Reading'), (3, 'Read'), (4, 'Abandoned')], default=None, null=True)),
                ('rate', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Horrible'), (2, 'Bad'), (3, 'Normal'), (4, 'Good'), (5, 'Very well')], default=None, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
        ),
    ]
