from urllib import response
from django.urls import reverse
from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.models import User

from Books.models import Book, UserBookRelation, CommentBook
from Books.views import *
from ..selectors import *

class TestBookServices(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

        self.book = Book.objects.create(name='some book')
        self.user = User.objects.create(username='user1',
                                        password='username123')
        self.comment = CommentBook.objects.create(book=self.book,
                                                  user=self.user,
                                                  body="Test comment")
        self.user2 = User.objects.create(username='user2', password='username123')
        self.user3 = User.objects.create(username='user3', password='username123')
        self.user4 = User.objects.create(username='user4', password='username123')
        self.user5 = User.objects.create(username='user5', password='username123')
        self.user6 = User.objects.create(username='user6', password='username123')


    def test_get_comment_data(self):
        """Test get limited amount of book comment"""
        self.comment.liked.add(self.user2)
        self.comment.disliked.add(self.user3)

        expected_data = {'data': [{
            'pk': self.comment.pk,
            'username': self.user.username,
            'comment': 'Test comment',
            'likes': 1,
            'dislikes': 1,
            'time_created': "03 June 2022",
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
                             'disliked': False}
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
                             'disliked': False}
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
                             'disliked': False}
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
                             'disliked': True}
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
                             'disliked': True}
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
                             'disliked': False}
        self.assertEquals(response, expected_response)

    def test_create_comment(self):
        response = create_comment(book_pk=self.book.pk,
                                  body='Test',
                                  user=self.user,)
        expected_response = {'username': self.user.username,
                             'comment': "Test",
                             'comment_pk': 2,
                             'time_created': '03 June 2022'}
        self.assertEquals(response, expected_response) 
        
    
    

    
