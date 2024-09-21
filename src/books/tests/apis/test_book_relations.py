import logging
from datetime import timedelta, datetime

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient

from books.models import Book, CommentBook, UserBookRelation
from genres.models import Genre
from users.models import User


class BookRelationsAPITests(APITestCase):
    def setUp(cls):
        logging.getLogger('django.request').setLevel(logging.ERROR)
        cls.book = Book.objects.create(name='some book')
        cls.user = User.objects.create(username='user1', password='username123', email="user1@gmail.com")
        cls.user2 = User.objects.create_user(username='user2', password='username123', email="user2@gmail.com")
        cls.user3 = User.objects.create_user(username='user3', password='username123', email="user3@gmail.com")
        cls.user4 = User.objects.create_user(username='user4', password='username123', email="user4@gmail.com")
        cls.comment = CommentBook.objects.create(book=cls.book, user=cls.user, body="Test comment")
        cls.comment2 = CommentBook.objects.create(book=cls.book, user=cls.user, body="Test comment2")
        cls.comment3 = CommentBook.objects.create(book=cls.book, user=cls.user, body="Test comment3")
    
    def test_comment_create(self):
        self.client.force_login(self.user4)
        r = self.client.post(reverse("create-comment"), data={"book": self.book.id, "body": "Test comment4"})
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.data['body'], "Test comment4")
        self.assertEqual(r.data['user']['username'], "user4")
    
    def test_comment_list(self):
        r = self.client.get(reverse("get-comments", args=(self.book.id,)))
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.data['results'][0]['body'], self.comment3.body)
        self.assertEqual(r.data['results'][1]['body'], self.comment2.body)
        self.assertEqual(r.data['results'][2]['body'], self.comment.body)
    
    def test_like_dislike_comment(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("like-comment", args=(self.comment.id,)))
        self.client.force_login(self.user2)
        r = self.client.get(reverse("dislike-comment", args=(self.comment.id,)))
        self.client.force_login(self.user3)
        r = self.client.get(reverse("dislike-comment", args=(self.comment.id,)))
        self.client.force_login(self.user4)
        r = self.client.get(reverse("dislike-comment", args=(self.comment.id,)))
        
        
        r = self.client.get(reverse("get-comments", args=(self.book.id,)))
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.data['results'][2]['likes'], 1)
        self.assertEqual(r.data['results'][2]['dislikes'], 3)
        self.assertEqual(r.data['results'][2]['liked'], False)
        self.assertEqual(r.data['results'][2]['disliked'], True)
        
    def test_delete_dislike_comment(self):
        """Delete dislike if already user disliked comment"""
        self.client.force_login(self.user4)
        r = self.client.get(reverse("dislike-comment", args=(self.comment.id,)))
        
        r = self.client.get(reverse("get-comments", args=(self.book.id,)))
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.data['results'][2]['dislikes'], 1)
        self.assertEqual(r.data['results'][2]['disliked'], True)
        
        r = self.client.get(reverse("dislike-comment", args=(self.comment.id,)))
        
        r = self.client.get(reverse("get-comments", args=(self.book.id,)))
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.data['results'][2]['dislikes'], 0)
        self.assertEqual(r.data['results'][2]['disliked'], False)
        
    def test_delete_like_comment(self):
        """Delete like if already user liked comment"""
        self.client.force_login(self.user4)
        r = self.client.get(reverse("like-comment", args=(self.comment.id,)))
        
        r = self.client.get(reverse("get-comments", args=(self.book.id,)))
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.data['results'][2]['likes'], 1)
        self.assertEqual(r.data['results'][2]['liked'], True)
        
        r = self.client.get(reverse("like-comment", args=(self.comment.id,)))
        
        r = self.client.get(reverse("get-comments", args=(self.book.id,)))
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.data['results'][2]['likes'], 0)
        self.assertEqual(r.data['results'][2]['liked'], False)
    
    def test_delete_comment(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("delete-comment", args=(self.comment.id,)))
        self.assertEqual(200, r.status_code)
        
        with self.assertRaises(CommentBook.DoesNotExist):
            CommentBook.objects.get(id=self.comment.id)
            
    def test_delete_comment_if_not_author(self):
        self.client.force_login(self.user4)
        r = self.client.get(reverse("delete-comment", args=(self.comment.id,)))
        self.assertEqual(403, r.status_code)
        
        self.assertTrue(CommentBook.objects.filter(id=self.comment.id).exists())
        
    def test_get_user_bookmark(self):
        self.client.force_login(self.user)
        UserBookRelation.objects.create(
            user=self.user, book=self.book, bookmarks=1
        )
        r = self.client.get(reverse("get-bookmarks", args=(self.book.id,)))
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.data['bookmarks'], 1)
        
    def test_create_user_bookmark(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse("create-bookmarks"), data={"book": self.book.id, "bookmarks": 2})
        
        self.assertEqual(200, r.status_code, r.data)
        self.assertEqual(r.data['bookmarks'], 2)
        self.assertEqual(UserBookRelation.objects.get(book=self.book, user=self.user).bookmarks, 2)

    def test_get_book_avg_rating(self):
        self.client.force_login(self.user)
        UserBookRelation.objects.create(
            user=self.user, book=self.book, rate=2
        )
        UserBookRelation.objects.create(
            user=self.user2, book=self.book, rate=4
        )
        UserBookRelation.objects.create(
            user=self.user3, book=self.book, rate=3
        )
        r = self.client.get(reverse("get-rating", args=(self.book.id,)))
        self.assertEqual(200, r.status_code, r.data)
        self.assertEqual(r.data['avg_rating'], 3.0)
        
    def test_create_book_rate(self):
        UserBookRelation.objects.create(
            user=self.user3, book=self.book, rate=1
        )
        self.client.force_login(self.user)
        r = self.client.post(reverse("create-rating"), data={"book": self.book.id, "rate": 2})
        
        self.assertEqual(200, r.status_code, r.data)
        self.assertEqual(r.data['avg_rating'], 1.5)
        self.assertEqual(UserBookRelation.objects.get(book=self.book, user=self.user).rate, 2)
