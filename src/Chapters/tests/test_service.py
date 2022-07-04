from datetime import datetime, timedelta

from django.test import TestCase, Client
from django.utils import timezone

from users.models import CustomUser, Profile
from Books.models import Book, UserBookRelation, CommentBook
from Chapters.models import Chapter, BookNotification

from ..service import *

class TestBookServices(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

        cls.book = Book.objects.create(name='some book')
        cls.user = CustomUser.objects.create(username='user1',
                                              password='username123')
        cls.chapter = Chapter.objects.create(
            book=cls.book,
            title='Something',
            body='There is something too',
        )

    def test_create_notification_with_relation(self):
        """Test if creating notification when user set bookmark"""
        UserBookRelation.objects.create(
            book=self.book,
            user=self.user,
            bookmarks=3,
        )
        create_notification(
            book=self.book,
            time=self.chapter.time_created,
            message='New chapter created!'
        )
        notification = BookNotification.objects.get(
            book=self.book,
            user=self.user
        )
        
        self.assertTrue(notification)
    def test_create_notification_without_relation(self):
        """Test if creating notification when user not follow"""
        UserBookRelation.objects.create(
            book=self.book,
            user=self.user,
        )
        create_notification(
            book=self.book,
            time=self.chapter.time_created,
            message='New chapter created!'
        )
        notification = BookNotification.objects.filter(
            book=self.book,
            user=self.user
        ).exists()
        
        self.assertFalse(notification)

    def test_create_notification_without_following_relation(self):
        """Test if creating notification when user not follow"""
        Profile.objects.filter(user=self.user).update(
            notificate_planning=False,
            notificate_reading=True,
            notificate_read=False,
            notificate_abandonded=False
        )
        UserBookRelation.objects.create(
            book=self.book,
            user=self.user,
            bookmarks=3
        )
        create_notification(
            book=self.book,
            time=self.chapter.time_created,
            message='New chapter created!'
        )
        notification = BookNotification.objects.filter(
            book=self.book,
            user=self.user
        ).exists()
        
        self.assertFalse(notification)


    def test_get_time_yesterday(self):
        tz = timezone.get_current_timezone()
        time_yesterday = datetime.now(tz=tz) - timedelta(
            days=1,
            seconds=3,
            )
        
        expected_response = 'Yesterday'
        real_response = get_time_verbally(time_yesterday)
        self.assertEquals(expected_response, real_response)
    
    def test_get_time_today(self):
        tz = timezone.get_current_timezone()
        time = datetime.now(tz=tz) - timedelta(
            hours=5,
            )
        
        expected_response = 'Today'
        real_response = get_time_verbally(time)
        self.assertEquals(expected_response, real_response)

    def test_get_time_today(self):
        tz = timezone.get_current_timezone()
        time = datetime.now(tz=tz) - timedelta(
            hours=15,
            )
        
        expected_response = '15 hours ago'
        real_response = get_time_verbally(time)
        self.assertEquals(expected_response, real_response)


    def test_get_time_week_ago(self):
        tz = timezone.get_current_timezone()
        time = datetime.now(tz=tz) - timedelta(
            days=8,
            seconds=3,
            )
        
        expected_response = 'Week ago'
        real_response = get_time_verbally(time)
        self.assertEquals(expected_response, real_response)

    def test_get_time_two_weeks_ago(self):
        tz = timezone.get_current_timezone()
        time = datetime.now(tz=tz) - timedelta(
            days=14,
            seconds=3,
            )
        
        expected_response = '2 weeks ago'
        real_response = get_time_verbally(time)
        self.assertEquals(expected_response, real_response)
    
    def test_get_time_month_ago(self):
        tz = timezone.get_current_timezone()
        time = datetime.now(tz=tz) - timedelta(
            days=31,
            seconds=3,
            )
        
        expected_response = 'Month ago'
        real_response = get_time_verbally(time)
        self.assertEquals(expected_response, real_response)

    def test_get_time_two_month_ago(self):
        tz = timezone.get_current_timezone()
        time = datetime.now(tz=tz) - timedelta(
            days=67,
            seconds=3,
            )
        
        expected_response = '2 months ago'
        real_response = get_time_verbally(time)
        self.assertEquals(expected_response, real_response)
