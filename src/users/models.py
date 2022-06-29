from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/',
                               default='default/user/b7647bef0d7011489f1c129bf01a2190.jpg')


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    age = models.PositiveSmallIntegerField(default=12)
    description = models.TextField(max_length=1000, blank=True)
    
    notificate_planning = models.BooleanField(default=True)
    notificate_reading = models.BooleanField(default=True)
    notificate_read = models.BooleanField(default=True)
    notificate_abandonded = models.BooleanField(default=True)
