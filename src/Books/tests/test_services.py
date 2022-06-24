from django.urls import reverse
from django.test import RequestFactory, TestCase, Client

from users.models import CustomUser
from Books.models import Book, UserBookRelation, CommentBook
from Books.views import *
from ..selectors import *

class TestBookServices(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

        self.book = Book.objects.create(name='some book')
        self.user = CustomUser.objects.create(username='user1',
                                              password='username123')

    def test_selector_fetch_get_count_bookmarks_and_rating(self):
        """Test getting from db count of reading, abandonded, read and planning books"""
        user2 = CustomUser.objects.create(username='user2', password='username123', email='admin@gmail.com')
        user3 = CustomUser.objects.create(username='user3', password='username123', email='admin2@gmail.com')
        relation1 = UserBookRelation.objects.create(
                    book=self.book, user=self.user,
                    bookmarks=2
        )
        relation2 = UserBookRelation.objects.create(
                    book=self.book, user=user2,
                    bookmarks=3
        )
        relation3 = UserBookRelation.objects.create(
                    book=self.book, user=user3,
                    bookmarks=2
        )
        response = get_users_bookmarks_and_rating().get(pk=self.book.pk)
        response = {'plan_to_read': response.plan_to_read,
                    'reading': response.reading,
                    'read': response.read,
                    'abandonded': response.abandonded,
                    }
        expected_response = {'plan_to_read': 0,
                             'reading': 2,
                             'read': 1,
                             'abandonded': 0,
                             }
        self.assertEqual(response, expected_response)

    def test_get_avarage_rating_with_3_relations(self):
        """Testing avarage rating that make 3 users"""
        user2 = CustomUser.objects.create(username='user2', password='username123', email='admin@gmail.com')
        user3 = CustomUser.objects.create(username='user3', password='username123', email='admin2@gmail.com')
        UserBookRelation.objects.create(
                    book=self.book, user=self.user,
                    rate=2
        )
        UserBookRelation.objects.create(
                    book=self.book, user=user2,
                    rate=5
        )
        UserBookRelation.objects.create(
                    book=self.book, user=user3,
                    rate=2
        )
        response = get_average_rating(book_pk=self.book.pk)
        expected_response = 3.0
        self.assertEquals(response, expected_response, response)

    def test_get_bookmark_data(self):
        """Test getting bookmark from db"""
        UserBookRelation.objects.create(
                    book=self.book, user=self.user,
                    bookmarks=2
        )
        response = get_bookmark_data(book_pk=self.book.pk,
                                     user=self.user)
        expected_response = {'bookmark_value': 2}
        self.assertEquals(response, expected_response)
        
    def test_bookmark_add_to_book(self):
        """Test add user bookmark"""
        UserBookRelation.objects.create(
                    book=self.book, 
                    user=self.user,
        )

        response = bookmark_book(book_pk=self.book.pk,
                                 user=self.user,
                                 bookmark=2)
        expected_response = {'clicked': True, 'previous_bookmark': None}
        bookmark = get_bookmark_data(book_pk=self.book.pk,
                                     user=self.user)
        expected_bookmark = {'bookmark_value': 2}
        self.assertEquals(response, expected_response)
        self.assertEquals(bookmark, expected_bookmark)

    def test_bookmark_remove_to_book(self):
        """Test remove user bookmark"""
        UserBookRelation.objects.create(
                    book=self.book, 
                    user=self.user,
                    bookmarks=2
        )

        response = bookmark_book(book_pk=self.book.pk,
                                 user=self.user,
                                 bookmark=2)
        expected_response = {'clicked': False, 'previous_bookmark': 2}
        bookmark = get_bookmark_data(book_pk=self.book.pk,
                                     user=self.user)
        expected_bookmark = {'bookmark_value': None}
        self.assertEquals(response, expected_response)
        self.assertEquals(bookmark, expected_bookmark)

    
