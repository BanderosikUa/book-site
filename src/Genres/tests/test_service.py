from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from Books.models import Book, UserBookRelation, CommentBook
from Genres.models import Genre
from Books.views import *
from ..selectors import *
from Books.selectors import *

class TestBookServices(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

        self.book = Book.objects.create(name='some book')
        self.genre1 = Genre.objects.create(name='Philosophy')
        self.book.genre.add(self.genre1)
        self.book2 = Book.objects.create(name='some book2')
        self.book2.genre.add(self.genre1)

        self.user = User.objects.create(username='user1',
                                        password='username123')
        self.user2 = User.objects.create(username='user2',
                                         password='username123')
        self.user3 = User.objects.create(username='user3',
                                         password='username123')
        
        UserBookRelation.objects.create(
                    book=self.book, user=self.user,
                    bookmarks=2, rate=2
        )
        UserBookRelation.objects.create(
                    book=self.book, user=self.user2,
                    bookmarks=3, rate=4
        )
        UserBookRelation.objects.create(
                    book=self.book, user=self.user3,
                    bookmarks=2, rate=3
        )

        # book2
        UserBookRelation.objects.create(
                    book=self.book2, user=self.user,
                    bookmarks=2, rate=1
        )
        UserBookRelation.objects.create(
                    book=self.book2, user=self.user2,
                    bookmarks=3, rate=1
        )
        UserBookRelation.objects.create(
                    book=self.book2, user=self.user3,
                    bookmarks=2, rate=1
        )
