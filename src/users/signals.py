from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Profile


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
