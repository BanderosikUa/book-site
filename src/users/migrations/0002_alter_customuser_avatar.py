# Generated by Django 4.0.4 on 2022-06-22 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='/media/default/user/b7647bef0d7011489f1c129bf01a2190.jpg', upload_to='users/%Y/%m/%d/'),
        ),
    ]
