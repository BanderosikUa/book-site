from datetime import datetime

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from Books.models import Book, CommentBook, UserBookRelation
from Books.views import *
from django.contrib.auth.models import User
from users.models import CustomUser
from ..selectors import *


class TestBookServices(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

        self.book = Book.objects.create(name='some book')
        self.user = CustomUser.objects.create(username='user1', password='username123', email='admin@gmail.com')
        self.comment = CommentBook.objects.create(book=self.book,
                                                  user=self.user,
                                                  body="Test comment")
        self.user2 = CustomUser.objects.create(username='user2', password='username123', email='admin1@gmail.com')
        self.user3 = CustomUser.objects.create(username='user3', password='username123', email='admin2@gmail.com')
        self.user4 = CustomUser.objects.create(username='user4', password='username123', email='admin3@gmail.com')
        self.user5 = CustomUser.objects.create(username='user5', password='username123', email='admin4@gmail.com')
        self.user6 = CustomUser.objects.create(username='user6', password='username123', email='admin5@gmail.com')
        self.time_today = datetime.now().strftime("%d %B %Y")


    def test_get_comment_data(self):
        """Test get limited amount of book comment"""
        self.comment.liked.add(self.user2)
        self.comment.disliked.add(self.user3)

        expected_data = {'data': [{
            'pk': self.comment.pk,
            'username': self.user.username,
            'avatar': self.user.avatar.url,
            'comment': 'Test comment',
            'likes': 1,
            'dislikes': 1,
            'time_created': self.time_today,
            'liked': False,
            'disliked': False,
        }], 'size': 1}
        data = get_comment_data(book_pk=self.book.pk,
                                num_comments=3,
                                user=self.user)
        self.assertEquals(data, expected_data)

    def test_like_book_comment(self):
        """Test like book comment """
        self.comment.liked.add(self.user2)
        self.comment.disliked.add(self.user4, self.user5, self.user6)
        response = like_book_comment(book_pk=self.book.pk,
                                     comment_pk=self.comment.pk,
                                     user=self.user3)
        expected_response = {'likes': 2,
                             'dislikes': 3,
                             'liked': True,
                             'disliked': False,
                             'user': True}
        self.assertEquals(response, expected_response)

    def test_like_book_comment_delete_dislike(self):
        """Test if user already have dislike on comment, delete it,
        and add like"""
        self.comment.liked.add(self.user2)
        self.comment.disliked.add(self.user4, self.user5, self.user6, self.user3)
        response = like_book_comment(book_pk=self.book.pk,
                                     comment_pk=self.comment.pk,
                                     user=self.user3)
        expected_response = {'likes': 2,
                             'dislikes': 3,
                             'liked': True,
                             'disliked': False,
                             'user': True}
        self.assertEquals(response, expected_response)
    
    def test_like_book_comment_delete_like(self):
        """Test if user already have like and delete it"""
        self.comment.liked.add(self.user2, self.user3)
        self.comment.disliked.add(self.user4, self.user5, self.user6)
        response = like_book_comment(book_pk=self.book.pk,
                                     comment_pk=self.comment.pk,
                                     user=self.user3)
        expected_response = {'likes': 1,
                             'dislikes': 3,
                             'liked': False,
                             'disliked': False,
                             'user': True}
        self.assertEquals(response, expected_response)

    def test_dislike_book_comment(self):
        """Test dislike book comment """
        self.comment.liked.add(self.user2)
        self.comment.disliked.add(self.user4, self.user5, self.user6)
        response = dislike_book_comment(book_pk=self.book.pk,
                                        comment_pk=self.comment.pk,
                                        user=self.user3)
        expected_response = {'likes': 1,
                             'dislikes': 4,
                             'liked': False,
                             'disliked': True,
                             'user': True}
        self.assertEquals(response, expected_response)

    def test_dislike_book_comment_delete_like(self):
        """Test if user already have like on comment, delete it,
        and add dislike"""
        self.comment.liked.add(self.user2, self.user3)
        self.comment.disliked.add(self.user4, self.user5, self.user6)
        response = dislike_book_comment(book_pk=self.book.pk,
                                        comment_pk=self.comment.pk,
                                        user=self.user3)
        expected_response = {'likes': 1,
                             'dislikes': 4,
                             'liked': False,
                             'disliked': True,
                             'user': True}
        self.assertEquals(response, expected_response)
    
    def test_dislike_book_comment_delete_dislike(self):
        """Test if user already have dislike and delete it"""
        self.comment.liked.add(self.user2, self.user3)
        self.comment.disliked.add(self.user4, self.user5, self.user6)
        response = dislike_book_comment(book_pk=self.book.pk,
                                        comment_pk=self.comment.pk,
                                        user=self.user4)
        expected_response = {'likes': 2,
                             'dislikes': 2,
                             'liked': False,
                             'disliked': False,
                             'user': True}
        self.assertEquals(response, expected_response)

    def test_create_comment(self):
        """Test creating comment"""
        response = create_comment(book_pk=self.book.pk,
                                  body='Test',
                                  user=self.user,)
        expected_response = {'username': self.user.username,
                             'avatar': self.user.avatar.url,
                             'comment': "Test",
                             'pk': response['pk'],
                             'time_created': self.time_today,
                             'dislikes': 0,
                             'likes': 0,
                             'user': True
                             }
        self.assertEquals(response, expected_response) 
        
    
    

    
