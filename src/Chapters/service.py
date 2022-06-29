from datetime import date, datetime, timedelta, tzinfo

from django.utils import timezone

from Books.models import UserBookRelation, Book
from users.models import CustomUser
from .models import Chapter, BookNotification


def create_notification(book: Book, time: datetime, message: str) -> None:
    """Creating notification for all user who bookmarking that"""
    relations = UserBookRelation.objects.filter(book=book)\
                                        .only('user')
    for relation in relations:
        user = relation.user
        profile = user.profile
        if relation.bookmarks:
            notifications = (
                profile.notificate_planning,
                profile.notificate_reading,
                profile.notificate_read,
                profile.notificate_abandonded
            )
            if notifications[relation.bookmarks-1]:
                notification = BookNotification.objects.create(
                    book=book,
                    user=user,
                    text_notification=message,
                    time=time
                )


def add_notification_to_navbar(user: CustomUser) -> list[dict]:
    notifications = BookNotification.objects.filter(user=user)\
                                            .select_related('book')\
                                            .only(
                                                'book__photo',
                                                'book__name',
                                                'book__slug',
                                                'text_notification',
                                                'time',
                                                'pk'
                                                )
    size = notifications.count()
    data = []
    for notification in notifications:
        item = {
            'url': notification.book.get_absolute_url(),
            'photo': notification.book.photo.url,
            'message': notification.text_notification,
            'time': get_time(notification.time),
            'pk': notification.pk,
        }
        data.append(item)
    return {'data': data, 'size': size}

def get_time(time_comparing: datetime):
    time_now = timezone.now()
    time_ago = time_now - time_comparing
    days = time_ago.days
    if days >= 1:
        if days >= 7:
            if days >= 30:
                month = days // 30
                return f'{month} months ago' if month > 1 else 'Month ago'
            weeks = days // 7
            return f'{weeks} weeks ago' if weeks > 1 else 'Week ago'
        return f'{days} days ago' if days >= 2 else 'Yesterday'
    else:
        return 'Today'
