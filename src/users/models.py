from django.db import models
from django.contrib.auth.models import AbstractUser

AGE_CATEGORY = [('12', '12+'),
                ('14', '14+'),
                ('16', '16+'),
                ('18', '18+')
                ]

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/',
                               default='default/user/b7647bef0d7011489f1c129bf01a2190.jpg')
    age = models.CharField(max_length=3, default='12', choices=AGE_CATEGORY)
