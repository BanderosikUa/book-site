# Generated by Django 4.0.4 on 2022-05-26 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0005_alter_userbookrelation_bookmarks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbookrelation',
            name='bookmarks',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Plan to read'), (2, 'Reading'), (3, 'Read'), (4, 'Abandonded')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='userbookrelation',
            name='rate',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Nothing'), (1, 'Horrible'), (2, 'Bad'), (3, 'Normal'), (4, 'Good'), (5, 'Very well')], default=None, null=True),
        ),
    ]
