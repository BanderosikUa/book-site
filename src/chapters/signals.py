from django.dispatch import receiver
from django.db.models.signals import post_save

from books.models import UserBookRelation
from users.models import CustomUser
from .models import Chapter, BookNotification
from .service import create_notification


@receiver(post_save, sender=Chapter)
def post_save_chapter(created, **kwargs):
    """Create notification object if user
    has any notificate setting in profile"""
    instance = kwargs.get('instance')
    if created:
        message = f"<p class='h6 mb-0'>New chapter:</p><p class='h6 mb-0'>{instance.title}</p>"
        create_notification(
            book=instance.book,
            time=instance.time_created,
            message=message
        )
