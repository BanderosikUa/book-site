# Generated by Django 4.0.4 on 2022-06-28 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notificate_abandonded',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='notificate_planning',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='notificate_read',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='notificate_reading',
            field=models.BooleanField(default=True),
        ),
    ]
