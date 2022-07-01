from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from unidecode import unidecode
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/',
                               default='default/user/b7647bef0d7011489f1c129bf01a2190.jpg')
    slug = models.SlugField(null=True, blank=True,
                            max_length=255, validators=[validate_slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            name = unidecode(self.username)
            self.slug = slugify(name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile', args=(self.slug,))


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
